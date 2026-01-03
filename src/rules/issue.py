from dataclasses import dataclass


@dataclass
class Issue:
    name: str
    severity: str
    confidence: str
    evidence: dict