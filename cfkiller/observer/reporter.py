# cfkiller/observer/reporter.py
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime
from .metrics import MetricsCollector

class PDFReporter:
    def __init__(self, client_name: str = "Cliente Confidencial", logo_path: str = None):
        self.client = client_name
        self.logo = logo_path or "logo.png"
        self.date = datetime.now().strftime("%d de %B de %Y")
        self.template_dir = os.path.dirname(__file__)
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def generate(self, stats: dict, target: str, duration: int, mode: str):
        template = self.env.get_template("report_template.html")
        
        html_content = template.render(
            client=self.client,
            date=self.date,
            target=target,
            duration=duration,
            mode=mode.upper(),
            stats=stats,
            rps=stats.get("rps", 0),
            total_requests=stats.get("requests", 0),
            cf_blocked=stats.get("blocked", 0),
            recommendation=self._get_recommendation(stats, mode)
        )

        filename = f"reports/CFKiller_Report_{self.client.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        os.makedirs("reports", exist_ok=True)
        
        HTML(string=html_content, base_url=self.template_dir).write_pdf(filename)
        print(f"\nReporte profesional generado: {filename}")
        return filename

    def _get_recommendation(self, stats, mode):
        if mode == "rapidreset" and stats["rps"] > 50000:
            return "CRÍTICO: Servidor vulnerable a HTTP/2 Rapid Reset (CVE-2023-44487). Aplicar parche urgente."
        elif stats["blocked"] / max(stats["requests"], 1) > 0.7:
            return "WAF efectivo. Bot Management bien configurado."
        else:
            return "Configuración segura, pero revisar rate limiting y caching."

# Template HTML (guardar como report_template.html al lado)
"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f9f9f9; }
        .header { text-align: center; border-bottom: 4px solid #d32f2f; padding-bottom: 20px; }
        .logo { height: 80px; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #d32f2f; color: white; }
        .critical { background-color: #ffebee; border-left: 6px solid #d32f2f; padding: 15px; }
    </style>
</head>
<body>
    <div class="header">
        {% if logo %}<img src="{{ logo }}" class="logo">{% endif %}
        <h1>CFKiller v4.0 – Informe de Stress Testing</h1>
        <p><strong>Cliente:</strong> {{ client }} | <strong>Fecha:</strong> {{ date }}</p>
    </div>
    <h2>Objetivo: {{ target }}</h2>
    <p><strong>Modo de ataque:</strong> {{ mode }} | <strong>Duración:</strong> {{ duration }} segundos</p>

    <table>
        <tr><th>Métrica</th><th>Valor</th></tr>
        <tr><td>Requests totales</td><td>{{ total_requests | int }}</td></tr>
        <tr><td>RPS máximo</td><td>{{ rps | int }}</td></tr>
        <tr><td>Bloqueados por Cloudflare</td><td>{{ cf_blocked | int }}</td></tr>
    </table>

    <div class="critical">
        <h3>Conclusión y Recomendación</h3>
        <p>{{ recommendation }}</p>
    </div>
</body>
</html>
"""