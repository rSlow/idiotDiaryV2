from fastapi import FastAPI

from apps.not_working_place.http_app.routers import nwp_router
from http_server.webhook import webhook_router

app = FastAPI()

app.include_router(webhook_router)
app.include_router(nwp_router)
