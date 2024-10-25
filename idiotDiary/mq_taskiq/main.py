# import asyncio
#
# from taskiq_aio_pika import AioPikaBroker
# from taskiq_redis import RedisAsyncResultBackend
#
# redis_async_result = RedisAsyncResultBackend(
#     redis_url="redis://:redispassword@localhost:1002/0",
# )
#
# # Or you can use PubSubBroker if you need broadcasting
# broker = AioPikaBroker(
#     url="amqp://rabbituser:rabbitpassword@127.0.0.1:1004/",
# ).with_result_backend(redis_async_result)
#
#
# @broker.task
# async def best_task_ever() -> None:
#     """Solve all problems in the world."""
#     await asyncio.sleep(5.5)
#     print("All problems are solved!")
#
#
# async def main():
#     await broker.startup()
#
#     print("Starting tasks")
#
#     task = await best_task_ever.kiq()
#     result = await task.wait_result()
#
#     print(result)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())

import asyncio

from idiotDiary.mq_taskiq.broker import broker
from idiotDiary.mq_taskiq.tasks import add_one


async def main() -> None:
    # Never forget to call startup in the beginning.
    await broker.startup()
    # Send the task to the broker.
    task = await add_one.kiq(1)
    # Wait for the result.
    result = await task.wait_result()
    print(f"Task execution took: {result.execution_time} seconds.")
    if not result.is_err:
        print(f"Returned value: {result.return_value}")
    else:
        print("Error found while executing task.")
    await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
