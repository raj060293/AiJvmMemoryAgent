import csv
from pathlib import Path
from typing import List

from agent.confidence_scorer import ConfidenceScorer
from agent.fix_template_resolver import FixTemplateResolver
from agent.llm_explainer import LLMExplainer
from facts.store import FactStore
from rules import issue
from rules.classloader_leak_rule import ClassLoaderLeakRule
from rules.issue import Issue
from rules.large_retained_class_rule import LargeRetainedClassRule
from rules.static_cache_leak_rule import StaticCacheLeakRule
from rules.threadlocal_leak_rule import ThreadLocalLeakRule
from tools.csv_parsers.dominator_parser import enrich_with_retained_size
from tools.csv_parsers.gc_roots_parser import parse_gc_roots
from tools.csv_parsers.histogram_parser import parse_histogram
from tools.mat_runner import MatRunner

class MemoryAnalysisAgent:

    """
    Orchestrates the full JVM memory analysis workflow:
    Heap -> Facts -> Rules -> Explanation
    """

    def __init__(self, mat_exec: str):
        self.mat_runner = MatRunner(mat_exec)
        self.rules = [
            LargeRetainedClassRule(threshold_pct=40.0),
            StaticCacheLeakRule(retained_heap_threshold_pct=30.0),
            ThreadLocalLeakRule(retained_heap_threshold_pct=20.0),
            ClassLoaderLeakRule(retained_heap_threshold_pct=15.0)
        ]
        self.fix_resolver = FixTemplateResolver()
        self.explainer = LLMExplainer()
        self.confidence_scorer = ConfidenceScorer()

    def analyze(self, heap_path: str) -> None:

        """
        Entry point for heap analysis
        """

        print(f"Analyzing Heap Dump{heap_path}",heap_path)
        heap_path = Path(heap_path)
        if not heap_path.exists():
            raise FileNotFoundError(heap_path)

        out_dir = Path("mat-output")
        out_dir.mkdir(exist_ok=True)

        self.mat_runner.run_reports(str(heap_path), str(out_dir))

        fact_store = self._extract_facts(out_dir)
        issues = self._run_rules(fact_store)
        report = self._explain_issues(issues)
        self._print_report(report)

    # -----------------------------
    # Internal orchestration steps
    # -----------------------------

    def _extract_facts(self, out_dir: Path) -> FactStore:

        """
        Extract all facts from heap model
        """
        store = FactStore()
        histogram_csv = out_dir / "histogram.csv"
        dominator_csv = out_dir / "dominator_csv"
        gc_roots_csv = out_dir / "gc_roots.csv"

        total_heap_mb = self._estimate_total_heap_mb(histogram_csv)

        parse_histogram(histogram_csv, total_heap_mb, store)
        enrich_with_retained_size(dominator_csv, store, total_heap_mb)
        parse_gc_roots(gc_roots_csv, store)
        return store

    def _estimate_total_heap_mb(self, histogram_csv: Path):
        """
        Estimate total heap size from histogram CSV
        """

        total_bytes = 0
        with open(histogram_csv, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total_bytes+= int(row["Shallow Heap"])

        return total_bytes / (1024*1024)

    def _run_rules(self, fact_store):
        """
        Run all rules against the fact store
        """
        issues: List[Issue] = []

        for rule in self.rules:
            detected = rule.apply(fact_store)
            issues.extend(detected)
        return issues

    def _enrich_issues(self, issues: List[Issue], fact_store: FactStore) -> None:
        """
        Uses the LLM explainer to convert issues to explanations
        """
        if not issues:
            return

        # -----------------
        # Confidence
        # -----------------

        for issue in issues:
            score, bucket = self.confidence_scorer.score(issue, fact_store)
            issue.confidence_score = score
            issue.confidence = bucket

        # -----------------
        # Fix templates
        # -----------------

        for issue in issues:
            self.fix_resolver.resolve(issue)

        # -----------------
        # Explanations (LLM or fallback)
        # -----------------

        self.explainer.explain(issues)


    def _print_report(self, issues: List[Issue]) -> None:
        """
        Prints a simple human-readable report to console
        """

        print("\n========== JVM Memory Analysis Report ==========")

        if not issues:
            print("✔ Heap looks healthy. No major issues detected.")
            print("===============================================\n")
            return

        for issue in issues:
            print(f"\n Issue:{issue.name}")
            print(f"    Severity    : {issue.severity}")
            print(f"    Confidence  : {issue.confidence} ({issue.confidence_score}%)")
            print(f"    Summary     : {issue.fix.summary}")

            print("   Recommended Actions:")
            for action in issue.fix.actions:
                print(f"     - {action}")

            if issue.explanation:
                print("\n   Explanation:")
                print(issue.explanation["text"])

            print("\n===============================================\n")

