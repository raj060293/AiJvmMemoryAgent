import csv

from facts.ownership import ClassOwnershipFact
from facts.store import FactStore


def parse_gc_roots(csv_path, fact_store: FactStore):
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            root_type = row["Root Type"]

            if root_type not in ("STATIC", "THREAD", "CLASSLOADER"):
                continue

            fact_store.add(
                ClassOwnershipFact(
                    class_name=row["Class Name"],
                    owner_type=root_type,
                    owner_details=row["Details"]
                )
            )