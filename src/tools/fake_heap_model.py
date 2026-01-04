class FakeHeapClass:
    def __init__(self, name, count, shallow, retained):
        self.name = name
        self.instance_count = count,
        self.shallow_size_mb = shallow
        self.retained_size_mb = retained


class FakeHeapModel:
    total_heap_mb = 1024

    def get_classes(self):
        return[
            FakeHeapClass("java.util.HashMap", 120000, 50, 600),
            FakeHeapClass("byte[]", 80000, 30, 200),
        ]