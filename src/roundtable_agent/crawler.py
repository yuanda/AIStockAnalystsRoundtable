from __future__ import annotations

import json
import os
from urllib import request

from .models import CrawlerConfig


class OpenCrawlerClient:
    """Open crawler integration (compatible with Firecrawl-like scrape APIs)."""

    def __init__(self, config: CrawlerConfig):
        self.config = config

    def scrape(self, url: str) -> str:
        provider = self.config.provider.lower().strip()
        if provider in {"", "none"}:
            return ""

        api_key = os.getenv(self.config.api_key_env) if self.config.api_key_env else ""
        if provider == "firecrawl":
            return self._firecrawl_scrape(url=url, api_key=api_key)

        return f"[未支持的 crawler provider: {self.config.provider}]"

    def _firecrawl_scrape(self, url: str, api_key: str) -> str:
        if not self.config.base_url:
            return "[Firecrawl 未配置 base_url]"
        if not api_key:
            return f"[Firecrawl 未检测到密钥环境变量 {self.config.api_key_env}]"

        payload = {
            "url": url,
            "formats": ["markdown"],
            "onlyMainContent": True,
        }
        req = request.Request(
            f"{self.config.base_url.rstrip('/')}/v1/scrape",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            return f"[Firecrawl 抓取失败: {exc}]"

        markdown = body.get("data", {}).get("markdown", "")
        return markdown[:20_000]
