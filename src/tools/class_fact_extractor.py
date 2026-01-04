from facts.class_level import ClassMemoryFact
from facts.store import FactStore
from tools.heap_model import HeapModel


class ClassFactExtractor:

    def extract(self, heap_model: HeapModel, fact_store: FactStore):
        total_heap_mb = heap_model.total_heap_mb

        for cls in heap_model.get_classes():
            retained_mb = cls.retained_size_mb
            pct = (retained_mb/total_heap_mb) * 100

            fact_store.add(
                ClassMemoryFact(
                    class_name=cls.name,
                    instance_count=cls.instance_count,
                    shallow_size_mb=cls.shallow_size_mb,
                    retained_size_mb= retained_mb,
                    retained_heap_pct=pct
                )
            )

