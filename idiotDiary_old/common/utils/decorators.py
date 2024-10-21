import asyncio
from functools import wraps
from typing import TypeVar, Coroutine, Callable, Type, ParamSpec, Optional, Awaitable

T = TypeVar('T', covariant=True)
P = ParamSpec("P")


def coro_timer(timeout: int | float, exc: Optional[Type[Exception] | Exception] = None):
    def decorator(coro: Callable[P, Coroutine[None, None, T]]) -> T:
        @wraps(coro)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            try:
                return await asyncio.wait_for(coro(*args, **kwargs), timeout=timeout)
            except asyncio.TimeoutError:
                if exc is not None:
                    raise exc

        return wrapper

    return decorator


def to_async_thread(func: Callable[P, T]) -> Callable[P, Awaitable[T]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper
