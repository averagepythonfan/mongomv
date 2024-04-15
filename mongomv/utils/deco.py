from functools import wraps


def not_none_return(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is not None:
            return result
        else:
            raise TypeError("Result is None.")
    return wrapper
