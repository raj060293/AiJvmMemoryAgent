from facts.base import Fact


class FactStore:

    def __init__(self):
        self.facts = []

    def add(self, fact):
        self.facts.append(fact)

    def get_all(self):
        return self.facts

    def get_by_type(self, fact_type):
        return [f for f in self.facts if isinstance(f, fact_type)]
