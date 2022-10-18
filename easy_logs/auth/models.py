from __future__ import annotations

from dataclasses import dataclass

@dataclass
class User:
    name: str
    password: str | None = None

    is_active: bool = True
    is_anonymous: bool = False
    is_authenticated: bool = True

    def get_id(self) -> str:
        return self.name
