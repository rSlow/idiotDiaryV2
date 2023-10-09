from pathlib import Path

from environs import Env


def get_env(env_dir: Path):
    env = Env()
    env_files = [
        "aiogram.env",
        "postgres.env",
        "redis.env",
    ]
    for env_file in env_files:
        env.read_env(str(env_dir / env_file))

    return env
