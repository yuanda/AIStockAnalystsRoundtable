from __future__ import annotations

from datetime import datetime

from .orchestrator import PhaseResult


DISCLAIMER = "本报告仅供研究参考，不构成任何投资建议。市场有风险，投资需谨慎。"


def build_report(company: str, symbol: str, results: list[PhaseResult]) -> str:
    header = [
        f"# {company}（{symbol}）投资价值分析报告",
        "",
        f"- 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 免责声明：{DISCLAIMER}",
        "",
        "---",
        "",
    ]

    sections: list[str] = []
    for item in results:
        sections.append(f"## {item.title}")
        sections.append(item.conclusion)
        sections.append("")
        sections.append("<details><summary>查看辩论过程</summary>")
        sections.append("")
        sections.append(item.transcript)
        sections.append("")
        sections.append("</details>")
        sections.append("")

    return "\n".join(header + sections)
