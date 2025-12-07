"""
A small, well-formed LLM wrapper that reads settings from config.config.CONFIG
and supports both the modern OpenAI client (openai>=1.0.0) and the legacy
openai.ChatCompletion API as a fallback.
"""

from typing import Optional
import openai
from config.config import CONFIG

client = None
try:
    # Modern client
    from openai import OpenAI

    api_key = CONFIG.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key) if api_key else OpenAI()
except Exception:
    # Fall back to legacy module-level client
    openai.api_key = CONFIG.get("OPENAI_API_KEY")
    client = None


def _call_with_new_client(system_prompt: str, user_prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=CONFIG.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=CONFIG.get("TEMPERATURE", 0.3),
        )
        choice = response.choices[0]
        if hasattr(choice, "message") and choice.message:
            return getattr(choice.message, "content", "")
        return getattr(choice, "text", "")
    except Exception as e:
        return f"[LLM ERROR] {str(e)}"


def _call_with_legacy(system_prompt: str, user_prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=CONFIG.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=CONFIG.get("TEMPERATURE", 0.3),
        )
        choice = response.choices[0]
        if isinstance(choice, dict) and "message" in choice:
            return choice["message"].get("content", "")
        if hasattr(choice, "message") and choice.message:
            return choice.message.get("content", "")
        return getattr(choice, "text", "") or ""
    except Exception as e:
        return f"[LLM ERROR] {str(e)}"


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """Public: call the configured LLM client (new or legacy)."""
    if client is not None:
        return _call_with_new_client(system_prompt, user_prompt)
    return _call_with_legacy(system_prompt, user_prompt)



