import re

def sanitize_prompt(prompt: str) -> str:
    blacklist = [
        r"ignore previous", r"override", r"system:", r"assistant:",
        r"run command", r"execute", r"delete", r"shutdown"
    ]
    clean = prompt.lower()
    for b in blacklist:
        clean = re.sub(b, "[blocked]", clean)
    return clean
