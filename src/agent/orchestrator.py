from typing import List

from agent.llm_explainer import LLMExplainer
from facts.heap_summary import HeapSummaryFact
from facts.store import FactStore
from rules.heap_usage_rule import HighHeapUsageRule
from rules.issue import Issue
from rules.large_retained_class_rule import LargeRetainedClassRule
from rules.static_cache_leak_rule import StaticCacheLeakRule
from tools.class_fact_extractor import ClassFactExtractor
from tools.fake_heap_model import FakeHeapModel
from tools.heap_model import HeapModel
from tools.ownership_fact_extractor import OwnershipFactExtractor


class MemoryAnalysisAgent:

    """
    Orchestrates the full JVM memory analysis workflow:
    Heap -> Facts -> Rules -> Explanation
    """

    def __init__(self):
        self.rules = [
            LargeRetainedClassRule(threshold_pct=40.0),
            StaticCacheLeakRule(retained_heap_threshold_pct=30.0)
        ]
        self.explainer = LLMExplainer()

    def analyze(self, heap_path: str):

        """
        Entry point for heap analysis
        """

        print(f"Analyzing Heap Dump{heap_path}",heap_path)

        heap = self._load_heap(heap_path)
        facts = self._extract_facts(heap)
        issues = self._run_rules(facts)
        report = self._explain_issues(issues)
        self._print_report(report)

    # -----------------------------
    # Internal orchestration steps
    # -----------------------------

    def _load_heap(self, heap_path: str) -> HeapModel:
        """
        Loads the heap dump and returns a HeapModel Abstraction

        For now, this uses FakeHeapModel.
        Later, this will be replaced with Eclipse MAT adapter
        """
        print("[Agent] Loading heap model")
        return FakeHeapModel()

    def _extract_facts(self, heap_model: HeapModel) -> FactStore:

        """
        Extract all facts from heap model
        """
        store = FactStore()

        #Class level facts
        class_extractor = ClassFactExtractor()
        class_extractor.extract(heap_model, store)

        # Ownership facts(Fake for now)
        OwnershipFactExtractor().extract(heap_model, store)

        return store

    def _run_rules(self, fact_store):
        """
        Run all rules against the fact store
        """
        issues: List[Issue] = []

        for rule in self.rules:
            issues.extend(rule.apply(fact_store))

        return issues

    def _explain_issues(self, issues: List[Issue]) -> List[str]:
        """
        Uses the LLM explainer to convert issues to explanations
        """
        if not issues:
            return ["Heap looks healthy. No major issues detected"]

        print("[Agent] Explaining issues")
        return self.explainer.explain(issues)

    def _print_report(self, report: List[str]) -> None:
        """
        Prints the final human-readable report.
        """
        print("\n========== Memory Analysis Report ==========")
        for line in report:
            print(f"- {line}")
        print("===========================================\n")
