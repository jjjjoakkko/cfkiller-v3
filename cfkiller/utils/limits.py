# cfkiller/utils/limits.py
import psutil

class ResourceGovernor:
    def __init__(self, max_cpu=85, max_ram=90, max_connections=50_000):
        self.limits = {"cpu": max_cpu, "ram": max_ram, "conn": max_connections}

    def check(self) -> bool:
        if psutil.cpu_percent() > self.limits["cpu"]:
            return False
        if psutil.virtual_memory().percent > self.limits["ram"]:
            return False
        return True