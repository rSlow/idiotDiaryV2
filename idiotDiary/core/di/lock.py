from dishka import Provider, Scope, provide

from ..utils.lock_factory import MemoryLockFactory, LockFactory


def create_lock_factory() -> LockFactory:
    return MemoryLockFactory()


class LockProvider(Provider):
    scope = Scope.APP

    @provide
    def get_lock_factory(self) -> LockFactory:
        return create_lock_factory()
