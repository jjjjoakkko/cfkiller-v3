# cfkiller/core/attacker.py
from abc import ABC, abstractmethod
from typing import Protocol

class Attacker(Protocol):
    @abstractmethod
    async def attack(self) -> None:
        """Ejecuta el ataque"""
        ...

    @abstractmethod
    def get_stats(self) -> dict:
        """Devuelve métricas del ataque"""
        ...