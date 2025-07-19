from datetime import datetime
import functools

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now()}] Executing: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[{datetime.now()}] Finished: {func.__name__}")
        return result
    return wrapper
