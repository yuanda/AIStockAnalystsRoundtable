from __future__ import annotations

from pathlib import Path
import tempfile

import gradio as gr

from .document_loader import combine_documents
from .models import AppConfig
from .orchestrator import RoundtableOrchestrator
from .report import build_report


def _render_discussions(results) -> str:
    blocks: list[str] = []
    for item in results:
        blocks.append(f"<details><summary>{item.title} - 查看讨论过程</summary>\n\n{item.transcript}\n\n</details>")
    return "\n\n".join(blocks)


def run_roundtable(company: str, symbol: str, config_path: str, files, urls_text: str):
    config = AppConfig.from_file(config_path)

    saved_paths: list[str] = []
    for f in files or []:
        saved_paths.append(f.name)

    evidence = combine_documents(saved_paths)
    urls = [line.strip() for line in (urls_text or "").splitlines() if line.strip()]

    orchestrator = RoundtableOrchestrator(config)
    results = orchestrator.run(
        company=company,
        symbol=symbol,
        evidence_context=evidence,
        source_urls=urls,
    )
    report = build_report(company, symbol, results)

    temp_dir = Path(tempfile.mkdtemp(prefix="roundtable_report_"))
    output = temp_dir / f"{symbol}_report.md"
    output.write_text(report, encoding="utf-8")
    return report, _render_discussions(results), str(output)


def create_app() -> gr.Blocks:
    with gr.Blocks(title="AI 金融分析师圆桌") as app:
        gr.Markdown("# AI 金融分析师圆桌（Web）")
        gr.Markdown("支持上传年报/图片等资料，支持 URL 交给 OpenCrawler 抓取，并可折叠查看讨论过程。")

        with gr.Row():
            company = gr.Textbox(label="公司名称", placeholder="Apple")
            symbol = gr.Textbox(label="股票代码", placeholder="AAPL")

        config_path = gr.Textbox(label="配置文件路径", value="config/models.json")
        files = gr.File(label="上传资料", file_count="multiple")
        urls_text = gr.Textbox(
            label="待抓取 URL（每行一个，可选）",
            lines=4,
            placeholder="https://example.com/10k",
        )

        run_btn = gr.Button("开始分析", variant="primary")

        report_output = gr.Markdown(label="最终报告")
        discussions_output = gr.Markdown(label="讨论过程（可折叠）")
        file_output = gr.File(label="下载报告")

        run_btn.click(
            fn=run_roundtable,
            inputs=[company, symbol, config_path, files, urls_text],
            outputs=[report_output, discussions_output, file_output],
        )

    return app


def main() -> None:
    app = create_app()
    app.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
