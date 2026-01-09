from facts.class_level import ClassMemoryFact
from facts.ownership import ClassOwnershipFact
from facts.store import FactStore
from rules.base import Rule
from rules.issue import Issue


class ClassLoaderLeakRule(Rule):

    """Detects Memory retained by ClassLoader GC roots,
    typically caused by application redeployment leaks
    """

    def __init__(self, retained_heap_threshold_pct: float = 15.0):
        self.retained_heap_threshold_pct = retained_heap_threshold_pct

    def apply(self, fact_store: FactStore):
        issues = []

        class_facts = fact_store.get_by_type(ClassMemoryFact)
        ownership_facts = fact_store.get_by_type(ClassOwnershipFact)

        classloader_owners = {}

        for ownership_fact in ownership_facts:
            if ownership_fact.owner_type == "CLASSLOADER":
                (classloader_owners.setdefault(ownership_fact.class_name, [])
                 .append(ownership_fact.owner_details))

        for class_fact in class_facts:
            if class_fact.retained_heap_pct < self.retained_heap_threshold_pct:
                continue

            loaders = classloader_owners.get(class_fact.class_name)
            if not loaders:
                continue

            issues.append(
                Issue(
                    name="Classloader Memory Leak",
                    severity="High",
                    confidence="High",
                    evidence={
                        "class_name": class_fact.class_name,
                        "retained_heap_pct": class_fact.retained_heap_pct,
                        "retained_size_mb": class_fact.retained_size_mb,
                        "classloaders": loaders[:5]
                    }

                )
            )
        return issues
