from facts.heap_summary import HeapSummaryFact
from facts.store import FactStore
from rules.heap_usage_rule import HighHeapUsage, HighHeapUsageRule


class MemoryAnalysisAgent:
    def analyze(self, heap_path: str):
        print(f"Analyzing Heap Dump{heap_path}",heap_path)
        heap = self.parse_heap(heap_path)
        facts = self.extract_facts(heap)
        issues = self.run_rules(facts)
        report = self.explain(issues)
        return report

    def extract_facts(self, heap):
        store = FactStore()
        store.add(
            HeapSummaryFact(
                total_heap_mb=1024,
                used_heap_mb=900,
                object_count=3_000_000
            )
        )
        return store

    def run_rules(self, fact_store):
        rule = HighHeapUsageRule()
        return rule.apply(fact_store)