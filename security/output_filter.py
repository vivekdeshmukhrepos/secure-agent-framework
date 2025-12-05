def filter_harmful_output(text: str) -> str:
    banned = ["hate", "kill", "racist", "violence"]
    for b in banned:
        if b in text.lower():
            return "[BLOCKED BY MODERATION]"
    return text
