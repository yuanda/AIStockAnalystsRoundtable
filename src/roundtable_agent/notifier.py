from __future__ import annotations

import json
import os
from dataclasses import dataclass
from urllib import request

from .models import NotifyConfig


@dataclass
class SendResult:
    channel: str
    ok: bool
    detail: str


class WebhookNotifier:
    def __init__(self, config: NotifyConfig):
        self.config = config

    def notify(self, title: str, content: str) -> list[SendResult]:
        results: list[SendResult] = []
        for channel, channel_cfg in {
            "wecom": self.config.wecom,
            "feishu": self.config.feishu,
            "discord": self.config.discord,
        }.items():
            if not channel_cfg.enabled:
                continue
            webhook = os.getenv(channel_cfg.webhook_url_env)
            if not webhook:
                results.append(SendResult(channel, False, f"缺少环境变量 {channel_cfg.webhook_url_env}"))
                continue
            results.append(self._send_webhook(channel, webhook, title, content))
        return results

    def _send_webhook(self, channel: str, webhook: str, title: str, content: str) -> SendResult:
        if channel in {"wecom", "feishu"}:
            payload = {"msg_type": "text", "content": {"text": f"{title}\n{content}"}}
        else:  # discord
            payload = {"content": f"**{title}**\n{content}"}

        req = request.Request(
            webhook,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=20):
                pass
        except Exception as exc:  # noqa: BLE001
            return SendResult(channel, False, str(exc))
        return SendResult(channel, True, "sent")
