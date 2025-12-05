import re

def mask_sensitive_data(text: str) -> str:
    text = re.sub(r"\b\d{10}\b", "[masked-phone]", text)
    text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+", "[masked-email]", text)
    text = re.sub(r"\b[0-9]{12}\b", "[masked-id]", text)
    return text
