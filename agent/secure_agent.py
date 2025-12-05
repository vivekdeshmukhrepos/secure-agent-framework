import re
from llm import call_llm
from config import settings

class SecureAgent:
    def __init__(self):
        self.last_log = ""

    # -----------------------------
    # Security Filters
    # -----------------------------
    def sanitize_prompt_injection(self, text: str) -> str:
        lowered = text.lower()
        if "ignore previous" in lowered or "override" in lowered or "ignore instructions" in lowered:
            return "[BLOCKED: Prompt Injection Attempt Detected]"
        return text

    def sanitize_data_leakage(self, text: str) -> str:
        original = text

        # Email Regex: catches all common cases
        email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        # Phone Regex: 10-digit sequences with optional separators
        phone_pattern = r"\b(?:\+91[-\s]?)?[0-9]{10}\b"

        sanitized = re.sub(email_pattern, "[EMAIL_MASKED]", text)
        sanitized = re.sub(phone_pattern, "[PHONE_MASKED]", sanitized)

        # If ANY sanitization happened → return formatted block
        if sanitized != original:
            return f"[BLOCKED]: {sanitized}"

        # Otherwise return original text
        return text

    def sanitize_model_inversion(self, text: str) -> str:
        lowered = text.lower()
        if "salary" in lowered or "internal policy" in lowered:
            return "[BLOCKED: Model Inversion Attempt]"
        return text

    def sanitize_harmful_output(self, text: str) -> str:
        if any(term in text.lower() for term in ["violence", "hate", "kill"]):
            return "[FILTERED: Harmful Content Blocked]"
        return text

    # -----------------------------
    # Security Pipeline
    # -----------------------------
    def apply_security(self, category: str, text: str):
        steps = []
        steps.append(f"Input: {text}")

        if category == "Prompt Injection":
            text = self.sanitize_prompt_injection(text)
            steps.append(f"[Prompt Injection Sanitization] → {text}")

        elif category == "Data Leakage":
            text = self.sanitize_data_leakage(text)
            steps.append(f"[Data Leakage Protection] → {text}")

        elif category == "Model Inversion":
            text = self.sanitize_model_inversion(text)
            steps.append(f"[Model Inversion Mitigation] → {text}")

        elif category == "Harmful / Biased Output":
            text = self.sanitize_harmful_output(text)
            steps.append(f"[Harmful Content Filter] → {text}")

        elif category == "Secure Summarizer":
            # Multi-layer sanitization for uploads
            text = self.sanitize_data_leakage(text)
            steps.append(f"[Data Leakage Protection] → {text}")
            text = self.sanitize_prompt_injection(text)
            steps.append(f"[Prompt Injection Sanitization] → {text}")

        return text, steps

    # -----------------------------
    # Direct Process (Used for Attack Tabs)
    # -----------------------------
    def process(self, category: str, user_text: str) -> str:
        sanitized_text, steps = self.apply_security(category, user_text)

        if "[BLOCKED" in sanitized_text or "[FILTERED" in sanitized_text:
            final_output = sanitized_text
            steps.append(f"Final Output: {final_output}")
            self.last_log = "\n".join(steps)
            return final_output

        result = call_llm(
            system_prompt=f"You are a secure AI agent handling: {category}. Apply all safe AI practices.",
            user_prompt=sanitized_text,
        )

        steps.append(f"LLM Output: {result}")
        self.last_log = "\n".join(steps)
        return result

    # -----------------------------
    # Advanced Agent Planner (For Summarizer)
    # -----------------------------
    def plan_and_execute(self, category: str, prompt: str) -> str:
        sanitized_prompt, steps = self.apply_security(category, prompt)

        steps.append("Planning: Generating summary safely...")

        result = call_llm(
            system_prompt="You are a secure summarization agent. Never reveal private data.",
            user_prompt=sanitized_prompt,
        )

        steps.append(f"Final Summary: {result}")

        self.last_log = "\n".join(steps)
        return result




# Export agent instance
agent = SecureAgent()
