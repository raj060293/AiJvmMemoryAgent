from dataclasses import dataclass
from typing import List

@dataclass
class FixTemplate:
    title: str
    summary: str
    actions: List[str]
    risks_if_ignored: str