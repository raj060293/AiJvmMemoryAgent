from dataclasses import dataclass

from facts.base import Fact

@dataclass(frozen = True)
class ClassHistogramFact(Fact):
    class_name: str
    instance_count: int
