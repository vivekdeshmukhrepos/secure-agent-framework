import random

def apply_dp_noise(text: str) -> str:
    if random.random() < 0.15:
        return text + " [dp-noise]"
    return text
