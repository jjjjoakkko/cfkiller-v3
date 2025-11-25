import pytest
from cfkiller.core.http2.rapid_reset import RapidResetAttacker


def test_connections_alias_and_get_stats():
    # Use the connections alias param and verify it maps to max_connections
    attacker = RapidResetAttacker(host="httpbin.org", connections=3, duration=1, intensity=1)
    assert attacker.max_connections == 3

    stats = attacker.get_stats()
    assert isinstance(stats, dict)
    assert set(stats.keys()) >= {"sent", "reset", "errors", "start_time", "rps"}
