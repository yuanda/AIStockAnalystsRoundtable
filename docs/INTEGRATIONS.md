# 推荐成熟组件（GitHub / Hugging Face）

以下是为“快速落地 + 可维护性”筛选的成熟方案：

## 文件读取与文档理解

- Unstructured（GitHub: `Unstructured-IO/unstructured`）
  - 统一处理 PDF/Office/HTML/图片，适合后续替换当前轻量 loader。
- Docling（GitHub: `DS4SD/docling`）
  - 在年报解析、表格/版面理解方面表现优秀。
- Hugging Face OCR 模型（如 `microsoft/trocr-*`）
  - 可替代本地 `pytesseract` 方案，提高复杂版面识别能力。

## OpenCrawler / 网页抓取

- Firecrawl（GitHub: `mendableai/firecrawl`）
  - 提供 API + 抓取质量稳定，当前代码已兼容其 scrape 接口。
- Crawl4AI（GitHub: `unclecode/crawl4ai`）
  - 适合构建本地可控 crawler 管线。

## 通信平台集成

- 企业微信机器人 Webhook（官方）
- 飞书机器人 Webhook（官方）
- Discord Webhook（官方）

> 当前仓库默认使用 webhook 路径，优点是实现快、依赖少、上线门槛低。
