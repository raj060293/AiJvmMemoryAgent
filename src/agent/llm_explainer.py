from typing import List

from agent.llm_clients.base import LLMClient
from rules.issue import Issue


class LLMExplainer:

    """
    Uses an LLM (OpenAI / Groq / etc.) to convert deterministic
    JVM memory analysis results into clear, human-friendly explanations.

    IMPORTANT:
    - The LLM does NOT detect issues
    - The LLM does NOT change severity or confidence
    - The LLM only explains and suggests example fixes
    """

    def __init__(self,  client: LLMClient = None):
        self.client = client

    def explain(self, issues: List[Issue]) -> None:
        for issue in issues:
            fix = issue.fix
            if fix is None:
                continue

            prompt = self._build_prompt(issue, fix)

            if self.client:
                text = self._call_llm(prompt)
                source = "llm"
            else:
                text = self._fallback_explanation(issue, fix)
                source = "deterministic"

            issue.explanation = {
                "source": source,
                "text": text
            }

    def _build_prompt(self, issue, fix) -> str:
        return f"""
        You are a **senior JVM performance and memory diagnostics expert**.

You are analyzing a Java heap dump that has already been processed
by a deterministic analysis engine (Eclipse MAT + rule-based logic).

  VERY IMPORTANT RULES (DO NOT VIOLATE):
- Do NOT question or change the detected issue type.
- Do NOT change severity or confidence.
- Do NOT invent additional root causes.
- Do NOT assume any framework (Spring, Tomcat, Netty, etc.).
- Do NOT modify user code directly.
- Any code you provide MUST be generic, illustrative examples only.
- You are explaining, not deciding.

--------------------------------------------------
ISSUE DETECTED
--------------------------------------------------
Type: {issue.name}
Severity: {issue.severity}
Confidence: {issue.confidence}

--------------------------------------------------
EVIDENCE (FACTS – DO NOT INTERPRET BEYOND THIS)
--------------------------------------------------
{issue.evidence}

--------------------------------------------------
FIX STRATEGY (ALREADY DECIDED – DO NOT CHANGE)
--------------------------------------------------
Summary:
{fix.summary}

Recommended Actions:
{chr(10).join("- " + a for a in fix.actions)}

Risk If Ignored:
{fix.risks_if_ignored}

--------------------------------------------------
YOUR TASK
--------------------------------------------------

Explain the issue to a Java developer in a **clear, structured way**.

Use the following structure **exactly**:

1️⃣ WHAT IS HAPPENING  
- Describe what is retaining memory.
- Explain it in simple JVM terms (GC roots, object lifetime).
- Do NOT repeat the evidence verbatim — interpret it.

2️⃣ WHY THIS HAPPENS  
- Explain the typical programming pattern that leads to this issue.
- Keep it generic and educational.
- No framework assumptions.

3️⃣ WHY THIS IS DANGEROUS  
- Explain long-term impact (heap growth, OOM, redeploy issues).
- Tie back to the JVM lifecycle.

4️⃣ HOW TO FIX IT (STRATEGY)  
- Explain the fix strategy conceptually.
- Map directly to the provided recommended actions.
- Do NOT introduce new strategies.

5️⃣ EXAMPLE CODE (ILLUSTRATIVE ONLY)  
- Provide small, generic Java examples.
- Show a ❌ problematic pattern and a ✅ safer alternative.
- Clearly state that this is an example, not production-ready code.

Tone guidelines:
- Calm, confident, mentor-like
- No fear-mongering
- No absolute claims
- Educational, not prescriptive

Remember:
You are helping a developer understand **why** this happened
and **how** to fix it safely.

Begin.
"""

    # ---------------------------------------------------------
    # Deterministic fallback (no LLM)
    # ---------------------------------------------------------

    def _fallback_explanation(self, issue, fix) -> str:
        return (
            f"Issue detected: {issue.name}\n\n"
            f"What is happening: \n{fix.summary}\n\n"
            f"Recommended actions:\n"
            + "\n".join(f" -{a}" for a in fix.actions)
            +"\n\n"
            f"Risk if ignored:\n{fix.risks_if_ignored}"
        )

    # ---------------------------------------------------------
    # LLM call (provider-agnostic)
    # ---------------------------------------------------------

    def _call_llm(self, prompt: str) -> str:
        return self.client.chat(prompt)
        



