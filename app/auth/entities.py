from dataclasses import dataclass


@dataclass(slots=True)
class Token:
    token: str
    token_type: str
