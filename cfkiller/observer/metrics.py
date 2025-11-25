# cfkiller/observer/metrics.py
import time
import structlog
import psutil
from dataclasses import dataclass
from typing import Dict, Any
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# ====================== PROMETHEUS ======================
REQUESTS_TOTAL = Counter(
    "cfkiller_requests_total",
    "Total de requests enviadas",
    ["attack_type"]
)
BYTES_SENT = Counter("cfkiller_bytes_sent", "Bytes enviados al target")
ERRORS_TOTAL = Counter("cfkiller_errors_total", "Errores totales", ["attack_type"])
CF_BLOCKED = Counter("cfkiller_cloudflare_blocked", "Bloqueos Cloudflare detectados")

# Gauges en tiempo real
CPU_USAGE = Gauge("cfkiller_cpu_percent", "Uso CPU del atacante")
RAM_USAGE = Gauge("cfkiller_ram_percent", "Uso RAM del atacante")
ACTIVE_CONNECTIONS = Gauge("cfkiller_active_connections", "Conexiones activas")

# Histograma de latencias (solo para uTLS y browser)
REQUEST_DURATION = Histogram(
    "cfkiller_request_duration_seconds",
    "Duración de requests",
    buckets=(0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, float("inf"))
)

# ====================== STRUCTLOG ======================
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory()
)

log = structlog.get_logger()

# ====================== METRICS COLLECTOR ======================
@dataclass
class MetricsCollector:
    attack_type: str
    start_time: float = time.time()

    def inc_request(self, blocked: bool = False):
        REQUESTS_TOTAL.labels(attack_type=self.attack_type).inc()
        if blocked:
            CF_BLOCKED.inc()

    def inc_error(self):
        ERRORS_TOTAL.labels(attack_type=self.attack_type).inc()

    def observe_duration(self, seconds: float):
        REQUEST_DURATION.observe(seconds)

    def update_system(self):
        CPU_USAGE.set(psutil.cpu_percent())
        RAM_USAGE.set(psutil.virtual_memory().percent())
        ACTIVE_CONNECTIONS.set(len(psutil.net_connections()))

    def log_event(self, event: str, **kwargs):
        log.info(event, attack_type=self.attack_type, **kwargs)

# Inicia servidor Prometheus en puerto 8000
def start_prometheus_server(port: int = 8000):
    start_http_server(port)
    log.info("Prometheus metrics server iniciado", port=port)