# Expose project configuration as `settings` so other modules can do:
#   from config import settings
# This loader prefers the project's `config/config.py` CONFIG dictionary.
try:
    from .config import CONFIG as settings
except Exception:
    settings = {
        "OPENAI_API_KEY": "sk-proj",   # ← Replace with real key
        "OPENAI_MODEL": "gpt-4o-mini",
        "TEMPERATURE": 0.3,
    }

__all__ = ["settings"]