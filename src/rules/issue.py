from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass
class Issue:

    #Created by rules
    name: str
    severity: str
    evidence: Dict[str, Any]

    #Added by confidence scorer
    confidence: Optional[str] = None
    confidence_score: Optional[int] = None

    #Added by fix resolver
    fix: Optional[Dict[str, Any]] = None

    #Added by LLM explainer
    explanation: Optional[Dict[str, Any]] = None