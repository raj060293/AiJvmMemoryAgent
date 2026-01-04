from facts.class_level import ClassMemoryFact
from facts.store import FactStore
from rules.base import Rule
from rules.issue import Issue


class LargeRetainedClassRule(Rule):
    """
    Detects classes that retain unsual amount of heap memory
    """

    def __init__(self, threshold_pct: float = 40.0):
        self.threshold_pct = threshold_pct

    def apply(self, fact_store: FactStore):
        issues = []

        class_facts = fact_store.get_by_type(ClassMemoryFact)

        for fact in class_facts:
            if fact.retained_heap_pct >= self.threshold_pct:
                issues.append(
                    Issue(
                        name= "Large Retained Class",
                        severity= "High",
                        confidence="High",
                        evidence= {
                            "class_name": fact.class_name,
                            "retained_heap_pct": fact.retained_heap_pct,
                            "retained_size_mb" : fact.retained_size_mb,
                            "instance_count": fact.instance_count
                        }

                    )
                )

        return issues