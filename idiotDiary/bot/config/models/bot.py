from __future__ import annotations

from dataclasses import dataclass

from .webhook import WebhookConfig


@dataclass
class BotConfig:
    token: str
    log_chat: int
    """tech chat for tech logs"""
    superusers: list[int]
    morph_service_url: str
    webhook: WebhookConfig | None = None
