from pathlib import Path

from .env import get_env

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV_DIR = BASE_DIR / "env"
ENV = get_env(env_dir=ENV_DIR)
