from functools import wraps

def sequence_wrapper():
    sequences = {}
    def outer():
        def decorator(fn):
            sequences[fn.__name__] = fn
            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)
            return inner
        return decorator
    outer.sequences = sequences
    return outer

sequence = sequence_wrapper()