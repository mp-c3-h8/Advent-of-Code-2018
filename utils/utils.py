from timeit import default_timer as timer
from functools import wraps
from typing import Any


def timed(desc: str | None = None):
    def decorator(fn):
        @wraps(fn)
        def wrap(*args: Any, **kwargs: Any) -> Any:
            s = timer()
            res = fn(*args, **kwargs)
            e = timer()
            if desc is not None:
                print(f"TIMED: ({desc}) -> ({e-s:2.4f} s)")
            else:
                print(f"TIMED: func ({fn.__name__}) -> ({e-s:2.4f} s)")

            return res
        return wrap
    return decorator
