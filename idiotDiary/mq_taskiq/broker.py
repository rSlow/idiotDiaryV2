from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

result_backend = RedisAsyncResultBackend(
    redis_url="redis://:redispassword@localhost:1002/1"
)

broker = AioPikaBroker(
    url="amqp://rabbituser:rabbitpassword@127.0.0.1:1004/",
    qos=30,
).with_result_backend(result_backend)
