import csv

from facts.class_level import ClassMemoryFact
from facts.store import FactStore


def enrich_with_retained_size(csv_path, fact_store: FactStore, total_heap_mb):
    retained_by_class = {}

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            retained_by_class[row["Class Name"]] = (
                float(row["Retained Heap"]) / (1024*1024)
            )
        for fact in fact_store.get_by_type(ClassMemoryFact):
            retained = retained_by_class.get(fact.class_name, 0.0)
            pct = (retained / total_heap_mb) * 100 if total_heap_mb else 0.0

            updated = ClassMemoryFact(
                class_name= fact.class_name,
                instance_count= fact.instance_count,
                shallow_size_mb=fact.shallow_size_mb,
                retained_size_mb=retained,
                retained_heap_pct=pct
            )
            fact_store.replace(
                fact,
                updated
            )