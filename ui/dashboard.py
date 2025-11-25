# ui/dashboard.py
import streamlit as st
import requests
import time
from datetime import datetime
import pandas as pd

# Configuración página
st.set_page_config(page_title="CFKiller v4.0 – Live Dashboard", layout="wide")
st.title("CFKiller v4.0 – Centro de Mando en Vivo")
st.markdown("**Solo para pentest autorizado** • 2025 • Tu Nombre")

# Sidebar controles
with st.sidebar:
    st.header("Estado del ataque")
    attack_running = st.session_state.get("running", False)
    
    if st.button("Iniciar Prometheus (si no está corriendo)", disabled=attack_running):
        try:
            requests.get("http://localhost:8000", timeout=2)
        except:
            import subprocess
            subprocess.Popen(["python", "-c", "from cfkiller.observer.metrics import start_prometheus_server; start_prometheus_server()"])
            time.sleep(2)
    
    st.markdown("---")
    st.caption("Métricas en tiempo real desde http://localhost:8000")

# Layout principal
col1, col2, col3, col4 = st.columns(4)

placeholder = st.empty()
graph_placeholder = st.empty()

while True:
    try:
        # Métricas Prometheus
        metrics = requests.get("http://localhost:8000", timeout=2).text
        
        # Parseamos métricas clave
        def get_value(name: str):
            for line in metrics.splitlines():
                if line.startswith(name):
                    return float(line.split()[-1])
            return 0.0

        req_total = get_value("cfkiller_requests_total")
        blocked = get_value("cfkiller_cloudflare_blocked")
        errors = get_value("cfkiller_errors_total")
        rps = get_value("cfkiller_requests_total") / max(time.time() - st.session_state.get("start", time.time()), 1)

        with placeholder.container():
            col1.metric("Requests totales", f"{int(req_total):,}")
            col2.metric("RPS actual", f"{rps:,.0f}")
            col3.metric("Bloqueados CF", f"{int(blocked):,}", delta=None)
            col4.metric("Errores", f"{int(errors):,}")

            col5, col6, col7 = st.columns(3)
            col5.metric("CPU", f"{get_value('cfkiller_cpu_percent'):.1f}%")
            col6.metric("RAM", f"{get_value('cfkiller_ram_percent'):.1f}%")
            col7.metric("Conexiones activas", int(get_value('cfkiller_active_connections')))

        # Gráfico en vivo
        df = pd.DataFrame({
            "Tiempo": [datetime.now().strftime("%H:%M:%S")],
            "RPS": [rps],
            "Bloqueados": [blocked]
        })
        graph_placeholder.line_chart(df.set_index("Tiempo")["RPS"])

    except:
        st.warning("Esperando Prometheus en http://localhost:8000...")
    
    time.sleep(1)