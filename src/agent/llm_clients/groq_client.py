import os

from groq import Groq
from agent.llm_clients.base import LLMClient


class GroqClient(LLMClient):

    def __init__(self, model: str | None = None):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set")

        self.provider = "groq"
        self.model = model or os.getenv("GROQ_MODEL", "llama3-70b-8192")
        self.client = Groq(api_key = api_key)

    def chat(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role" : "system", "content": "You are a senior JVM performance engineer."},
                {"role":"user", "content":prompt}
            ]
        )
        return response.choices[0].message.content

