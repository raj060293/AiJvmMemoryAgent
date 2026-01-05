from facts.ownership import ClassOwnershipFact


class OwnershipFactExtractor:
    """
    Extracts Ownership facts(STATIC, THREAD, CLASSLOADER)
    """

    def extract(self, heap_model,fact_store):
        #Fake Data for now
        fact_store.add(
            ClassOwnershipFact(
                class_name="java.util.HashMap",
                owner_type="STATIC",
                owner_details="MyCache.cache"
            )
        )