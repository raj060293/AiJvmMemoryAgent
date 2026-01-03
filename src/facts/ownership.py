from dataclasses import dataclass

from facts.base import Fact

@dataclass(frozen = True)
class ClassOwnershipFact(Fact):
    class_name: str
    owner_type: str # STATIC, THREAD, CLASSLOADER
    owner_details: str