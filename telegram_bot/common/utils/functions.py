import asyncio
from datetime import datetime
from functools import wraps
from typing import TypeVar, Coroutine, Callable, Any, Type

from config import settings

_T = TypeVar('_T')


def get_now():
    return datetime.now().astimezone(tz=settings.TIMEZONE)


def coro_timer(timeout: int, exc: Type[Exception] | Exception | None = None):
    def decorator(func: Callable[[Any, Any], Coroutine[None, None, _T]]) -> _T:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            coro = func(*args, **kwargs)
            try:
                return await asyncio.wait_for(coro, timeout=timeout)
            except asyncio.TimeoutError:
                if exc is not None:
                    raise exc

        return wrapper

    return decorator
