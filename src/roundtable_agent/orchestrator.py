from __future__ import annotations

from dataclasses import dataclass

from .crawler import OpenCrawlerClient
from .llm_client import LLMClient
from .models import AppConfig
from .prompts import PHASES, system_prompt


@dataclass
class PhaseResult:
    title: str
    transcript: str
    conclusion: str


class RoundtableOrchestrator:
    def __init__(self, config: AppConfig):
        self.config = config
        self.clients = [LLMClient(m) for m in config.models]
        self.crawler = OpenCrawlerClient(config.crawler)

    def run(
        self,
        company: str,
        symbol: str,
        evidence_context: str = "",
        source_urls: list[str] | None = None,
    ) -> list[PhaseResult]:
        results: list[PhaseResult] = []
        context = evidence_context

        if source_urls:
            for url in source_urls:
                crawled = self.crawler.scrape(url)
                if crawled:
                    context += f"\n\n## 外部网页资料: {url}\n{crawled[:6000]}"

        for phase in PHASES:
            title = phase["title"]
            instruction = phase["instruction"]
            transcript_parts: list[str] = []

            round_context = context
            for round_idx in range(1, self.config.debate_rounds + 1):
                transcript_parts.append(f"### 第 {round_idx} 轮辩论")
                outputs: list[str] = []
                for client in self.clients:
                    prompt = self._build_phase_prompt(
                        company=company,
                        symbol=symbol,
                        phase_title=title,
                        instruction=instruction,
                        prior_context=round_context,
                        round_index=round_idx,
                        peers_summary="\n\n".join(outputs),
                    )
                    answer = client.complete(system_prompt(), prompt)
                    outputs.append(f"#### {client.config.name}\n{answer}")
                transcript_parts.extend(outputs)
                round_context += "\n\n" + "\n\n".join(outputs)

            conclusion = self._synthesize_phase(title, instruction, transcript_parts)
            context += f"\n\n## {title}\n{conclusion}"
            results.append(
                PhaseResult(title=title, transcript="\n\n".join(transcript_parts), conclusion=conclusion)
            )

        return results

    def _build_phase_prompt(
        self,
        company: str,
        symbol: str,
        phase_title: str,
        instruction: str,
        prior_context: str,
        round_index: int,
        peers_summary: str,
    ) -> str:
        return (
            f"目标公司: {company} ({symbol})\n"
            f"当前章节: {phase_title}\n"
            f"任务: {instruction}\n"
            f"当前轮次: 第{round_index}轮\n\n"
            "输出要求：\n"
            "- 先列关键事实与数据（可含估算，需标注假设）\n"
            "- 再给推理链路\n"
            "- 最后给结论与风险项\n"
            "- 对其他模型可能的偏差主动反驳\n\n"
            f"既有上下文：\n{prior_context[-8000:] if prior_context else '（无）'}\n\n"
            f"同轮其他模型观点摘要：\n{peers_summary if peers_summary else '（你是本轮首位发言）'}"
        )

    def _synthesize_phase(self, title: str, instruction: str, transcript_parts: list[str]) -> str:
        transcript = "\n\n".join(transcript_parts)[-12000:]
        synthesis_prompt = (
            f"请基于以下多模型辩论记录，输出章节《{title}》最终稿。\n"
            f"章节目标: {instruction}\n"
            "要求：\n"
            "1) 结构清晰，先数据后结论；\n"
            "2) 明确共识、分歧和待验证问题；\n"
            "3) 保持专业简洁；\n"
            "4) 以 markdown 输出小标题和要点。\n\n"
            f"辩论记录：\n{transcript}"
        )
        moderator = self.clients[0]
        return moderator.complete(system_prompt(), synthesis_prompt)
