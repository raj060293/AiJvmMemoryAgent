from abc import ABC, abstractmethod


class LLMClient(ABC):

    provider: str
    model: str

    @abstractmethod
    def chat(self, prompt: str) -> str:
        pass
