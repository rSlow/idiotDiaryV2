from pathlib import Path

from environs import Env


def get_env(env_dir: Path | None = None):
    env = Env()
    env_files = env_dir.glob('*.env')
    for env_file in env_files:
        env.read_env(str(env_dir / env_file))

    return env
