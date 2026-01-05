from facts.class_level import ClassMemoryFact
from facts.ownership import ClassOwnershipFact
from facts.store import FactStore
from rules.base import Rule
from rules.issue import Issue


class StaticCacheLeakRule(Rule):
    """
    Detects cache-like classes retained by static fields without eviction
    """
    def __init__(self, retained_heap_threshold_pct: float=30):
        self.retained_heap_threshold_pct = retained_heap_threshold_pct

    def apply(self, fact_store: FactStore):
        issues=[]
        class_facts = fact_store.get_by_type(ClassMemoryFact)
        ownership_facts = fact_store.get_by_type(ClassOwnershipFact)

        #Build quick lookup: class_name -> static owners

        static_owners = {
            fact.class_name: fact
            for fact in ownership_facts
            if fact.owner_type == "STATIC"
        }

        for class_fact in class_facts:

            #Is this class cache like
            if not self._looks_like_cache(class_fact.class_name):
                continue

            #Is memory retention high?
            if class_fact.retained_heap_pct < self.retained_heap_threshold_pct:
                continue

            #Is owned by a static field?
            ownership = static_owners.get(class_fact.class_name)
            if not ownership:
                continue

            #All signals matched, raise issue
            issues.append(
                Issue(
                    name = "Static Cache Leak",
                    severity="High",
                    confidence="High",
                    evidence= {
                        "class_name": class_fact.class_name,
                        "retained_heap_pct": class_fact.retained_heap_pct,
                        "retained_size_mb": class_fact.retained_size_mb,
                        "instance_count": class_fact.instance_count,
                        "static_owner": ownership.owner_details
                    }

                )
            )
        return issues


    def _looks_like_cache(self, class_name: str) -> bool:
        """
        Heuristic to identify cache-like classes
        """

        cache_keywords = [
            "Cache",
            "Map",
            "ConcurrentHashMap",
            "LRU",
            "Caffeine",
            "Guava"
        ]

        return any(keyword in class_name for keyword in cache_keywords)
