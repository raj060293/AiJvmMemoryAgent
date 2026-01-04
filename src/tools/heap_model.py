from typing import Protocol, Iterable


class HeapClass(Protocol):
    name: str
    instance_count: int
    shallow_size_mb: float
    retained_size_mb: float

class HeapModel(Protocol):
    total_heap_mb: float

    def get_classes(self) -> Iterable[HeapClass]:
        ...
