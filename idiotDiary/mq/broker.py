from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

from idiotDiary.core.config import setup_logging
from idiotDiary.core.config.parser.paths import get_paths
from idiotDiary.core.config.parser.retort import get_base_retort
from idiotDiary.mq.config.parser.main import load_config


def main():
    paths = get_paths()
    setup_logging(paths)

    retort = get_base_retort()
    mq_config = load_config(paths, retort)

    result_backend = RedisAsyncResultBackend(mq_config.result_backend.uri)
    _broker = (
        AioPikaBroker(url=mq_config.mq.uri, qos=1, max_priority=5)
        .with_result_backend(result_backend)
        .with_middlewares()
    )
    return _broker


broker = main()
