"""
Rate-Limit per Redis Sliding-Window.

Pro Label (= eingelogger Nutzer) zwei Limits: stündlich und täglich.
Implementiert als Sorted Set in Redis, in dem jeder Aufruf als Eintrag mit
Timestamp landet. Vor jedem Check werfen wir alte Einträge raus.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

import redis.asyncio as redis


@dataclass
class RateLimitConfig:
    per_hour: int
    per_day: int


class RateLimiter:
    def __init__(self, client: redis.Redis, config: RateLimitConfig) -> None:
        self._r = client
        self._cfg = config

    async def check_and_record(self, label: str) -> tuple[bool, str | None]:
        """Returns (allowed, reason). reason is set when blocked."""
        now = time.time()
        hour_key = f"rl:hour:{label}"
        day_key = f"rl:day:{label}"

        async with self._r.pipeline(transaction=False) as pipe:
            # Sliding-Windows aufräumen
            pipe.zremrangebyscore(hour_key, 0, now - 3600)
            pipe.zremrangebyscore(day_key, 0, now - 86400)
            pipe.zcard(hour_key)
            pipe.zcard(day_key)
            _, _, hour_count, day_count = await pipe.execute()

        if hour_count >= self._cfg.per_hour:
            return False, f"Stundenlimit erreicht ({self._cfg.per_hour}). Bitte später erneut versuchen."
        if day_count >= self._cfg.per_day:
            return False, f"Tageslimit erreicht ({self._cfg.per_day})."

        # Treffer eintragen (Score = Timestamp). Member muss eindeutig sein,
        # damit Mehrfach-Hits in derselben Sekunde nicht überschrieben werden.
        member = f"{now}:{os.urandom(4).hex()}"
        async with self._r.pipeline(transaction=False) as pipe:
            pipe.zadd(hour_key, {member: now})
            pipe.zadd(day_key, {member: now})
            pipe.expire(hour_key, 3600)
            pipe.expire(day_key, 86400)
            await pipe.execute()
        return True, None


def limiter_from_env(client: redis.Redis) -> RateLimiter:
    return RateLimiter(
        client,
        RateLimitConfig(
            per_hour=int(os.environ.get("RL_PER_HOUR", "20")),
            per_day=int(os.environ.get("RL_PER_DAY", "100")),
        ),
    )
