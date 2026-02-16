# AI Financial Analysts Roundtable Agent

一个“多模型圆桌辩论”的股票投资分析 Agent。
输入公司名称或股票代码，输出专业、结构化投资价值分析报告。

## 已支持能力

- 多模型协作（OpenAI-compatible API）
- 章节化辩论与总结（公司介绍 / 行业情况 / 公司具体情况 / 投资策略）
- Web 界面：上传 PDF / Word / PPT / Excel / 图片，在线运行并下载报告
- 折叠式讨论过程展示（`<details>`）
- OpenCrawler 集成：可把 URL 发给抓取引擎（当前内置 Firecrawl 兼容模式）
- 任务回传：企业微信 / 飞书 / Discord webhook 通知

## 为什么采用现成工具

为了节省实现时间并降低维护成本，本项目优先集成成熟生态：

- **文件读取**：`pypdf`、`python-docx`、`python-pptx`、`pandas/openpyxl`、`pytesseract`
- **Web UI**：`gradio`
- **网页抓取（OpenCrawler）**：Firecrawl API 兼容接口（可替换为 crawl4ai 等 GitHub 工具）
- **IM 通知**：企业微信/飞书/Discord webhook

## 快速开始（CLI）

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp config/models.example.json config/models.json
# 填好 API keys

roundtable-agent \
  --company "Apple" \
  --symbol AAPL \
  --config config/models.json \
  --files ./docs/aapl_10k.pdf ./docs/channel_check.xlsx \
  --urls https://www.apple.com/newsroom/ \
  --output report.md
```

## 启动 Web 页面

```bash
roundtable-agent-web
```

默认启动在 `http://localhost:7860`。

## 配置说明

见 `config/models.example.json`：

- `models[]`：多模型辩论配置
- `crawler`：OpenCrawler 配置（例如 Firecrawl）
- `notifications`：企业微信/飞书/Discord 任务消息配置

## 目录结构

- `src/roundtable_agent/webapp.py`：网页界面
- `src/roundtable_agent/document_loader.py`：多格式资料读取
- `src/roundtable_agent/crawler.py`：OpenCrawler 接口
- `src/roundtable_agent/notifier.py`：企业通信回传
- `src/roundtable_agent/orchestrator.py`：多模型辩论编排

## 注意

- 本项目用于研究与辅助决策，不构成投资建议。
- OCR 依赖系统安装（`tesseract`），未安装时会自动降级并提示。
