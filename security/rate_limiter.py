import time

_last_call_time = 0

def check_rate_limit() -> bool:
    global _last_call_time
    now = time.time()
    if now - _last_call_time < 1.5:  # 1.5 seconds throttle
        return False
    _last_call_time = now
    return True
