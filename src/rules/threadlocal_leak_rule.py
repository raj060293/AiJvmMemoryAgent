from facts.class_level import ClassMemoryFact
from facts.ownership import ClassOwnershipFact
from facts.store import FactStore
from rules.base import Rule
from rules.issue import Issue


class ThreadLocalLeakRule(Rule):

    """
    Detects memory retained by long-lived threads
    """

    def __init__(self, retained_heap_threshold_pct: float = 20.0):
        self.retained_heap_threshold_pct = retained_heap_threshold_pct

    def apply(self, fact_store: FactStore):
        issues = []

        class_facts = fact_store.get_by_type(ClassMemoryFact)
        ownership_facts = fact_store.get_by_type(ClassOwnershipFact)

        #Map class_name -> list of thread owners
        thread_owners = {}
        for ownership in ownership_facts:
            if ownership.owner_type == "THREAD":
                (thread_owners.setdefault(ownership.class_name , [])
                 .append(ownership.owner_details))

        for class_fact in  class_facts:
            if class_fact.retained_heap_pct < self.retained_heap_threshold_pct:
                continue

            threads = thread_owners.get(class_fact.class_name)
            if not threads:
                continue

            issues.append(
                Issue(
                    name = "ThreadLocal Memory Leak",
                    severity="High",
                    confidence="High",
                    evidence= {
                        "class_name": class_fact.class_name,
                        "retained_heap_pct" : class_fact.retained_heap_pct,
                        "retained_size_mb" : class_fact.retained_size_mb,
                        "threads" : threads[:5]
                    }
                )
            )
        return issues