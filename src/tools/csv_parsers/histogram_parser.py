import csv

from facts.class_level import ClassMemoryFact
from facts.store import FactStore


def parse_histogram(csv_path, total_heap_mb, fact_store: FactStore):
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            fact_store.add(
                ClassMemoryFact(
                    class_name= row["Class Name"],
                    instance_count=int(row["Objects"]),
                    shallow_size_mb=float(row["Shallow Heap"]) / (1024*1024),
                    retained_size_mb=0.0,
                    retained_heap_pct=0.0
                )
            )