from dataclasses import dataclass

from facts.base import Fact

@dataclass(frozen= True)
class ClassMemoryFact(Fact):
    class_name: str
    instance_count: int
    shallow_size_mb: float
    retained_size_mb: float
    retained_heap_pct: float

