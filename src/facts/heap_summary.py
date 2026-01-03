from dataclasses import dataclass

from facts.base import Fact

@dataclass(frozen = True)
class HeapSummaryFact(Fact):
    total_heap_mb: float
    used_heap_mb: float
    object_count: int
