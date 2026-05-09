"""
Auth via geteiltem Zugangscode.

Kein DB-State: gültige Codes stehen in der ENV `ACCESS_CODES`, Sessions
liegen als HMAC-signiertes Cookie im Browser.
"""

from __future__ import annotations

import os
import secrets
from dataclasses import dataclass

from itsdangerous import BadSignature, URLSafeTimedSerializer


COOKIE_NAME = "fakt_session"
COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 Tage


@dataclass(frozen=True)
class Session:
    label: str  # z.B. "berater_mueller"


class AuthService:
    def __init__(self, codes_env: str, session_secret: str) -> None:
        # Format: "code1:label1,code2:label2"
        self._codes: dict[str, str] = {}
        for entry in (codes_env or "").split(","):
            entry = entry.strip()
            if not entry or ":" not in entry:
                continue
            code, label = entry.split(":", 1)
            self._codes[code.strip()] = label.strip()
        self._serializer = URLSafeTimedSerializer(session_secret, salt="fakt-session")

    def verify_code(self, code: str) -> Session | None:
        # Constant-time-Vergleich gegen alle bekannten Codes.
        for known, label in self._codes.items():
            if secrets.compare_digest(code, known):
                return Session(label=label)
        return None

    def issue_cookie(self, session: Session) -> str:
        return self._serializer.dumps({"label": session.label})

    def read_cookie(self, value: str | None) -> Session | None:
        if not value:
            return None
        try:
            data = self._serializer.loads(value, max_age=COOKIE_MAX_AGE)
        except BadSignature:
            return None
        label = data.get("label") if isinstance(data, dict) else None
        if not isinstance(label, str):
            return None
        return Session(label=label)


def auth_from_env() -> AuthService:
    secret = os.environ.get("SESSION_SECRET")
    if not secret:
        raise RuntimeError("SESSION_SECRET nicht gesetzt")
    return AuthService(
        codes_env=os.environ.get("ACCESS_CODES", ""),
        session_secret=secret,
    )
