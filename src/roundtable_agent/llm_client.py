from __future__ import annotations

import json
import os
from dataclasses import asdict
from urllib import request, error

from .models import ModelConfig


class LLMClient:
    def __init__(self, config: ModelConfig):
        self.config = config

    def complete(self, system_prompt: str, user_prompt: str) -> str:
        api_key = os.getenv(self.config.api_key_env)
        if not api_key:
            return (
                f"[{self.config.name}] 未检测到环境变量 {self.config.api_key_env}，"
                "以下为离线占位输出：\n"
                "- 需要真实 API key 以执行模型辩论\n"
                "- 建议补充年报、行业数据库、估值假设后再运行"
            )

        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
        }
        raw = json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"{self.config.base_url.rstrip('/')}/chat/completions",
            data=raw,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            return f"[{self.config.name}] API 调用失败: HTTP {exc.code} {detail[:400]}"
        except Exception as exc:  # noqa: BLE001
            return f"[{self.config.name}] API 调用失败: {exc}"

        try:
            return body["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError):
            return (
                f"[{self.config.name}] 返回格式异常，原始响应片段："
                f"{json.dumps(body, ensure_ascii=False)[:400]}"
            )

    def metadata(self) -> dict:
        return asdict(self.config)
