from facts.ownership import ClassOwnershipFact
from facts.store import FactStore
from rules.issue import Issue


class ConfidenceScorer:
    """
    Computes confidence score for detected issues based on evidence
    """

    def score(self, issue: Issue, fact_store: FactStore) -> tuple[int, str]:
        score = 0
        evidence = issue.evidence
        class_name = evidence.get("class_name")

        # --------------------
        # Retained heap signal
        # --------------------

        retained_pct = evidence.get("retained_heap_pct", 0)

        if retained_pct >= 10:
            score+= 30
        if retained_pct >= 20:
            score+= 20

        # --------------------
        # Ownership strength
        # --------------------

        ownerships = [
           f for f in fact_store.get_by_type(ClassOwnershipFact)
           if f.class_name == class_name
        ]

        owner_types = {o.owner_type for o in ownerships}

        if "STATIC" in owner_types:
            score+= 30
        elif "THREAD" in owner_types:
            score+= 25
        elif "CLASSLOADER" in owner_types:
            score+=20

        # Multiple owners → more confidence
        if len(ownerships) > 1:
            score+= 10


        if self._looks_like_cache(class_name):
            score+=10

        return score, self._bucket(score)

    def _bucket(self, score: int) -> str:
        if score >= 70:
            return "High"
        elif score >= 40:
            return "Medium"
        else:
            return "Low"

    def _looks_like_cache(self, class_name: str | None) -> bool:
        if not class_name:
            return False

        keywords = ["Cache", "Map", "ConcurrentHashMap", "LRU", "Caffeine"]
        return any(k in class_name for k in keywords)
