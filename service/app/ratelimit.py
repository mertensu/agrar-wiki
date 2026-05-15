"""
Token-Budget pro Access-Label (Lifetime-Cap).

Jeder Access-Code (Label) hat ein einmaliges Token-Budget. Verbrauchte
Input+Output-Tokens werden in Redis als simpler Counter geführt
(`tokens:{label}`). Erreicht der Counter den Cap, ist das Label
gesperrt — Reset nur manuell (Redis-Key löschen oder neues Label).

Anders als ein Sliding-Window-Limit füllt sich das Budget nicht von
selbst auf. Wer durch ist, bleibt durch.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import redis.asyncio as redis


@dataclass
class TokenBudget:
    cap: int  # max. Tokens pro Label, Lifetime

    @classmethod
    def from_env(cls) -> "TokenBudget":
        return cls(cap=int(os.environ.get("TOKEN_CAP_PER_LABEL", "100000")))


class BudgetTracker:
    """Liest und erhöht den Lifetime-Tokenverbrauch pro Label in Redis."""

    def __init__(self, client: redis.Redis, budget: TokenBudget) -> None:
        self._r = client
        self._budget = budget

    @staticmethod
    def _key(label: str) -> str:
        return f"tokens:{label}"

    async def used(self, label: str) -> int:
        raw = await self._r.get(self._key(label))
        return int(raw or 0)

    async def check(self, label: str) -> tuple[bool, str | None, int, int]:
        """Vor jedem Call: ist noch Budget übrig?

        Returns (allowed, reason, used, cap). reason gesetzt, wenn blockiert.
        """
        used = await self.used(label)
        cap = self._budget.cap
        if used >= cap:
            reason = (
                f"Token-Budget aufgebraucht ({used:,} / {cap:,} Tokens). "
                "Bitte einen neuen Zugangscode anfordern."
            )
            return False, reason, used, cap
        return True, None, used, cap

    async def add(self, label: str, tokens: int) -> int:
        """Nach dem Call: tatsächlich verbrauchte Tokens addieren."""
        if tokens <= 0:
            return await self.used(label)
        return int(await self._r.incrby(self._key(label), tokens))


def tracker_from_env(client: redis.Redis) -> BudgetTracker:
    return BudgetTracker(client, TokenBudget.from_env())
