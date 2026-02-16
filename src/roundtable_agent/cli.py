from __future__ import annotations

import argparse
from pathlib import Path

from .document_loader import combine_documents
from .models import AppConfig
from .notifier import WebhookNotifier
from .orchestrator import RoundtableOrchestrator
from .report import build_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI 金融分析师圆桌 Agent")
    parser.add_argument("--company", required=True, help="公司名称，如 Apple")
    parser.add_argument("--symbol", required=True, help="股票代码，如 AAPL")
    parser.add_argument("--config", required=True, help="模型配置文件路径（JSON）")
    parser.add_argument("--output", default="report.md", help="输出报告文件")
    parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="可选，上传的资料文件路径（pdf/docx/pptx/xlsx/image 等）",
    )
    parser.add_argument(
        "--urls",
        nargs="*",
        default=[],
        help="可选，交给 OpenCrawler 抓取的 URL 列表",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = AppConfig.from_file(args.config)
    evidence = combine_documents(args.files)

    orchestrator = RoundtableOrchestrator(config)
    notifier = WebhookNotifier(config.notifications)
    notifier.notify(
        title="圆桌任务开始",
        content=f"公司: {args.company} ({args.symbol})，资料数: {len(args.files)}",
    )

    results = orchestrator.run(
        company=args.company,
        symbol=args.symbol,
        evidence_context=evidence,
        source_urls=args.urls,
    )
    report = build_report(args.company, args.symbol, results)

    output_path = Path(args.output)
    output_path.write_text(report, encoding="utf-8")

    notify_results = notifier.notify(
        title="圆桌任务完成",
        content=f"公司: {args.company} ({args.symbol})\n报告: {output_path.resolve()}",
    )
    print(f"报告已生成：{output_path.resolve()}")
    if notify_results:
        for item in notify_results:
            print(f"通知渠道 {item.channel}: {'成功' if item.ok else '失败'} - {item.detail}")


if __name__ == "__main__":
    main()
