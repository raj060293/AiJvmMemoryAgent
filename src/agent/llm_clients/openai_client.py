import os

from openai import OpenAI

from agent.llm_clients.base import LLMClient


class OpenAiClient(LLMClient):

    def __init__(self, model: str | None = None):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        self.provider = "openai"
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key = api_key)

    def chat(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role" : "system", "content" : "You are senior JVM performance engineer"},
                {"role" : "user", "content" : prompt}
            ],
        )
        return response.choices[0].message.content