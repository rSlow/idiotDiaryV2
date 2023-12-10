import asyncio
from functools import wraps, partial
from typing import TypeVar, Coroutine, Callable, Any, Type

_T = TypeVar('_T')


def coro_timer(timeout: int | float, exc: Type[Exception] | Exception | None = None):
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


def set_async(func: Callable[..., _T]) -> Callable[..., Coroutine[Any, Any, _T]]:
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, partial(func, *args, **kwargs)
        )

    return wrapper
