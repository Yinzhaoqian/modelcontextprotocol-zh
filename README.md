# Model Context Protocol 中文文档

Model Context Protocol（MCP）官方文档的**高质量中文镜像**。

> 源站：[modelcontextprotocol.io](https://modelcontextprotocol.io)　·　交付形态：Mintlify 中文站

本项目的目标是把官方技术文档**完整、准确**地映射为中文版本，与官方保持结构一致、语义一致、URL 一致、版本一致。中文文档是**镜像**，不是博客、教程、摘要或 AI 二次解读。

---

## 快速开始（本地预览）

本项目用 Mintlify 渲染，配置文件为 `translated/docs.json`，必须在 `translated/` 目录下启动：

```bash
cd translated && npx -y mint@latest dev
```

启动后访问 **http://localhost:3000**。首次启动会拉取 `mint` 包并构建，日志出现 `Local: http://localhost:3000` 即就绪。

更多说明（换端口、热重载、版本排查）见 **[docs/本地预览.md](docs/本地预览.md)**。

---

## 目录结构

```text
sources/            官方原始数据（sitemap / url-mapping / 原始 .md、.mdx）
translated/         中文镜像，按官方 Path 镜像目录
  docs.json         Mintlify 站点与导航配置
  docs/<版本>/**    文档正文（.mdx）
  specification/... 规范正文（.mdx）
docs/               项目规则与流程文档（见下）
glossary.json       全局技术术语表
AGENTS.md           项目总纲与核心原则
```

---

## 操作步骤 / 项目文档

开始任何翻译任务前，**必须先阅读**以下文档并严格遵守：

| 文档 | 说明 |
|------|------|
| [AGENTS.md](AGENTS.md) | 项目总纲：目标、核心原则、重要限制、任务执行优先级 |
| [docs/translation-rules.md](docs/translation-rules.md) | 翻译规范：代码/API/术语/规范性语言/URL 的处理规则与最终检查清单 |
| [docs/workflow.md](docs/workflow.md) | 标准工作流：从发现源站到生成报告的 9 个阶段 |
| [docs/plan.md](docs/plan.md) | 分批执行规划：批次划分（B0–B9）、子批顺序与进度追踪 |
| [docs/本地预览.md](docs/本地预览.md) | 本地预览：启动命令、热重载、端口与排查 |
| [glossary.json](glossary.json) | 全局术语表：确定后全站统一使用 |

### 标准工作流程（来自 [docs/workflow.md](docs/workflow.md)）

```text
阶段 1 发现源站 → 阶段 2 分析结构 → 阶段 3 建立 Sitemap → 阶段 4 建立 URL 映射
→ 阶段 5 建立术语表 → 阶段 6 逐页翻译 → 阶段 7 Source/Target 对照
→ 阶段 8 保存 → 阶段 9 生成报告
```

以「页面」为最小工作单位，每完成一页立即做 Source/Target 对照并修正。

### 核心原则（来自 [AGENTS.md](AGENTS.md)）

- **翻译，而不是改写**；映射，而不是重新解释
- 保留官方结构与技术语义，**不遗漏、不臆造**
- 优先级：技术准确性 > 语义完整性 > 结构一致性 > 术语一致性 > 中文自然度

---

## 翻译进度

版本化文档共 343 页，按批次推进（详见 [docs/plan.md](docs/plan.md)）。

| 批次 | 范围 | 状态 |
|------|------|------|
| B1 | docs/2026-07-28（latest 文档） | ✅ 完成 |
| B2 | specification/2026-07-28（latest 规范） | ✅ 完成 |
| B3 | 2025-11-25（文档 + 规范） | ✅ 完成 |
| B4 | 2025-06-18 | ⬜ 未开始 |
| B5 | 2025-03-26 | ⬜ 未开始 |
| B6 | 2024-11-05 | ⬜ 未开始 |
| B7 | 非版本化（community / registry / extensions 等） | ✅ 完成 |
| B8 | seps（提案文档） | ✅ 完成 |
| B9 | draft | ⬜ 未开始 |

> 完整进度表与验收口径见 [docs/plan.md](docs/plan.md)。
