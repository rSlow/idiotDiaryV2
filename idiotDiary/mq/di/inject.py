__all__ = [
    "inject",
    "error_inject"
]

from collections.abc import Callable
from inspect import Parameter
from typing import TypeVar, ParamSpec, cast, Any, Annotated, Generator

from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection
from dishka.integrations.taskiq import inject as taskiq_inject, CONTAINER_NAME
from taskiq import Context, TaskiqDepends, TaskiqMessage, TaskiqResult

from idiotDiary.mq.utils.types.di import ExceptionHandler

T = TypeVar("T")
P = ParamSpec("P")

InjectFunction = Callable[[Callable[P, T]], Callable[P, T]]

inject = cast(InjectFunction, taskiq_inject)


def _get_container(
        context: Annotated[Context, TaskiqDepends()]
) -> Generator[AsyncContainer, None, None]:
    yield context.message.labels[CONTAINER_NAME]


def sync_inject(func: Callable[..., Any]) -> Callable[..., Any]:
    annotation = Annotated[
        AsyncContainer, TaskiqDepends(_get_container),
    ]
    additional_params = [Parameter(
        name=CONTAINER_NAME,
        annotation=annotation,
        kind=Parameter.KEYWORD_ONLY,
    )]

    return wrap_injection(
        func=func,
        is_async=False,
        remove_depends=True,
        additional_params=additional_params,
        container_getter=lambda _, p: p[CONTAINER_NAME],
    )


def _error_container_getter(
        args: tuple[BaseException, TaskiqMessage, TaskiqResult],
        __: dict[str, Any]
):
    _exc, _msg, result = args
    return result.labels[CONTAINER_NAME]


def error_inject(func: ExceptionHandler) -> ExceptionHandler:
    return wrap_injection(  # noqa
        func=func,
        is_async=True,
        remove_depends=True,
        container_getter=_error_container_getter,
    )
