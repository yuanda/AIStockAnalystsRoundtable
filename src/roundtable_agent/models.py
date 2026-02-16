from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass
class ModelConfig:
    name: str
    provider: str
    base_url: str
    model: str
    api_key_env: str
    temperature: float = 0.2
    max_tokens: int = 1200


@dataclass
class CrawlerConfig:
    provider: str = "none"
    base_url: str = ""
    api_key_env: str = ""


@dataclass
class ChannelConfig:
    enabled: bool = False
    webhook_url_env: str = ""


@dataclass
class NotifyConfig:
    wecom: ChannelConfig
    feishu: ChannelConfig
    discord: ChannelConfig

    @classmethod
    def from_dict(cls, data: dict) -> "NotifyConfig":
        return cls(
            wecom=ChannelConfig(**data.get("wecom", {})),
            feishu=ChannelConfig(**data.get("feishu", {})),
            discord=ChannelConfig(**data.get("discord", {})),
        )


@dataclass
class AppConfig:
    models: list[ModelConfig]
    debate_rounds: int = 2
    crawler: CrawlerConfig = field(default_factory=CrawlerConfig)
    notifications: NotifyConfig = field(
        default_factory=lambda: NotifyConfig(
            wecom=ChannelConfig(),
            feishu=ChannelConfig(),
            discord=ChannelConfig(),
        )
    )

    @classmethod
    def from_file(cls, path: str) -> "AppConfig":
        config_path = Path(path)
        data = json.loads(config_path.read_text(encoding="utf-8"))
        models = [ModelConfig(**m) for m in data.get("models", [])]
        if not models:
            raise ValueError("配置文件中 models 不能为空")

        crawler = CrawlerConfig(**data.get("crawler", {}))
        notifications = NotifyConfig.from_dict(data.get("notifications", {}))
        return cls(
            models=models,
            debate_rounds=int(data.get("debate_rounds", 2)),
            crawler=crawler,
            notifications=notifications,
        )
