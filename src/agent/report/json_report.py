from datetime import datetime

from agent.llm_clients.base import LLMClient
from agent.report.models import (
AnalysisReport,
IssueReport,
ReportMetadata,
LLMMetadata
)
from agent.report.summary import build_summary


def generate_json_report(*, heap_dump: str,
                         issues,
                         llm_client: LLMClient,
                         agent_version: str = "1.0.0",
                         mat_version: str | None = None):
    llm_meta = (
        LLMMetadata(
            enabled=True,
            provider=llm_client.provider,
            model=llm_client.model,
        )
        if llm_client
        else LLMMetadata(enabled=False)
    )

    metadata = ReportMetadata(
        heap_dump = heap_dump,
        analyzed_at= datetime.utcnow().isoformat() + "Z",
        agent_version = agent_version,
        mat_version= mat_version,
        llm = llm_meta
    )
    issue_reports = []

    for issue in issues:
        issue_reports.append(
            IssueReport(
                type=issue.name,
                severity=issue.severity,
                confidence=issue.confidence,
                confidence_score = issue.confidence_score,
                affected_class=issue.evidence.get("class_name"),
                retained_heap_mb=issue.evidence.get("retained_size_mb", 0.0),
                retained_heap_pct=issue.evidence.get("retained_heap_pct", 0.0),
                ownership={
                    "type": issue.evidence.get("owner_type"),
                    "details": issue.evidence.get("owner_details")
                },
                evidence = issue.evidence,
                fix=issue.fix,
                explanation=issue.explanation
            )
        )
    summary = build_summary(issues)

    return AnalysisReport(
        metadata = metadata,
        summary=summary,
        issues = issue_reports
    )
