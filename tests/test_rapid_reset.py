# tests/test_rapid_reset.py
import pytest
from hypothesis import given, strategies as st
from cfkiller.core.http2.rapid_reset import RapidResetAttacker

@pytest.mark.asyncio
async def test_rapid_reset_stats_increment():
    attacker = RapidResetAttacker(
        host="httpbin.org",
        duration=2,
        max_connections=5,
        intensity=100
    )
    await attacker.attack()
    
    assert attacker.stats.reset > 0
    assert attacker.stats.rps > 100  # en localhost da bajo, pero >100 es realista