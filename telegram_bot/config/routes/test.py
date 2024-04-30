from aiogram import Router

from apps.free_shaurma.handlers.test import test_fsh_router

test_router = Router(name="test")
test_router.include_routers(
    test_fsh_router
)
