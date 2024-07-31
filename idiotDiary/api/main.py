import logging

from asgi_monitor.integrations.fastapi import setup_metrics, MetricsConfig
from fastapi import FastAPI

# from shvatka.api import routes, middlewares
from idiotDiaryV3.api.config.models.main import ApiConfig
from idiotDiaryV3.common.config.models.paths import Paths
from idiotDiaryV3.common.config.parser.paths import get_paths as get_common_paths

logger = logging.getLogger(__name__)


def create_app(config: ApiConfig) -> FastAPI:
    app = FastAPI()
    # app.include_router(routes.setup())
    # middlewares.setup(app, config)
    setup_metrics(
        app,
        MetricsConfig(
            app_name=config.app.name,
            include_metrics_endpoint=True,
            include_trace_exemplar=True,
        ),
    )

    return app


def get_paths() -> Paths:
    return get_common_paths("API_PATH")
