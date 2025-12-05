from security.prompt_sanitizer import sanitize_prompt
from security.data_masking import mask_sensitive_data
from security.output_filter import filter_harmful_output
from security.dp_noise import apply_dp_noise
from security.rate_limiter import check_rate_limit

# These are functions the agent can call in secure_agent.py

def tool_sanitize(text: str) -> str:
return sanitize_prompt(text)

def tool_mask(text: str) -> str:
return mask_sensitive_data(text)

def tool_filter(text: str) -> str:
return filter_harmful_output(text)

def tool_dp(text: str) -> str:
return apply_dp_noise(text)

def tool_rate() -> bool:
return check_rate_limit()
