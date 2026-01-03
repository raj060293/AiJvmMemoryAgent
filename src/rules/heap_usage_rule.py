from facts.heap_summary import HeapSummaryFact
from facts.store import FactStore
from rules.base import Rule
from rules.issue import Issue


class HighHeapUsageRule(Rule):
    def apply(self, fact_store: FactStore):
        issues = []
        summaries = fact_store.get_by_type(HeapSummaryFact)

        for summary in summaries:
            usage_pct = summary.used_heap_mb / summary.total_heap_mb

            if usage_pct > 0.8:
                issues.append(
                    Issue(
                        name= "High Heap Usage",
                        severity = "High",
                        confidence="High",
                        evidence={"usage_pct": usage_pct}
                    )
                )
        return issues