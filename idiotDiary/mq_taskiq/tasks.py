import time
from dataclasses import dataclass
from typing import Any

from idiotDiary.mq_taskiq.broker import broker


@dataclass
class TaskResult:
    name: str
    value: Any


@broker.task
def add_one(value: int) -> TaskResult:
    time.sleep(5)
    result = value + 1
    return TaskResult(name="add one", value=result)
