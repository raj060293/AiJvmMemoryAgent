from dataclasses import dataclass
from typing import Optional, Dict, Any, List


@dataclass
class LLMMetadata:
    enabled:bool
    provider: Optional[str] = None
    model: Optional[str] = None

@dataclass
class ReportMetadata:
    heap_dump: str
    analyzed_at: str
    agent_version: str
    mat_version: Optional[str]
    llm: LLMMetadata

@dataclass
class IssueReport:
    type: str
    severity: str
    confidence: str
    confidence_score: int
    affected_class: str
    retained_heap_mb: float
    retained_heap_pct: float
    ownership: Dict[str, Any]
    evidence: Dict[str, Any]
    fix: Dict[str, Any]
    explanation: Dict[str, Any]

@dataclass
class AnalysisReport:
    metadata: ReportMetadata
    summary: Dict[str, Any]
    issues: List[IssueReport]
