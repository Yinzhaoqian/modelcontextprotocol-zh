# Model Context Protocol 中文文档

Model Context Protocol（MCP）官方文档的**高质量中文镜像**。

> 源站：[modelcontextprotocol.io](https://modelcontextprotocol.io)　·　在线站点：**[mcp-zh.com](https://mcp-zh.com)**　·　技术栈：Astro Starlight（纯静态）

本项目的目标是把官方技术文档**完整、准确**地映射为中文版本，与官方保持结构一致、语义一致、URL 一致、版本一致。中文文档是**镜像**，不是博客、教程、摘要或 AI 二次解读。

---

## 架构

```text
translated/   ← 唯一真源：中文 .mdx（Mintlify 格式）+ docs.json 导航
     │
     │ scripts/migrate_mintlify_to_starlight.py   （组件转换 / 资源复制 / 生成侧边栏）
     ▼
web/          ← Astro Starlight 工程（生成内容不入库）
     │ npm run build
     ▼
web/dist/     ← 纯静态产物
     │ GitHub Actions → rsync
     ▼
RackNerd 服务器（Caddy 提供服务 + 自动 HTTPS）→ https://mcp-zh.com
```

- **`translated/` 是唯一真源**。翻译只改这里；`web/` 下的内容由迁移脚本生成，已在 `.gitignore` 中排除。
- 迁移脚本把 Mintlify 专有组件转换为 Starlight 语法：`Note/Warning`→提示框、`Card`→`LinkCard`、`Steps`/`Tabs`/`Accordion`、`Frame`、`Tree`，mermaid 图客户端渲染。
- 已接入 **Google Analytics 4**；首页为 Starlight splash。

---

## 本地预览

需要 **Node ≥ 22.12** 与 Python 3。

```bash
# 1. 生成 Starlight 内容（translated/ -> web/）
python scripts/migrate_mintlify_to_starlight.py

# 2. 安装依赖并启动开发服务器
cd web && npm install && npm run dev
```

启动后访问 **http://localhost:4321**。构建静态产物用 `npm run build`（输出到 `web/dist/`）。

> 改动 `translated/` 后需重新运行迁移脚本，`web/` 才会更新。

---

## 部署

推送到 `main` 后，GitHub Actions 自动构建并部署到服务器。完整步骤（DNS / Caddy / SSH 密钥 / GitHub Secrets）见 **[docs/部署.md](docs/部署.md)**。

- CI 工作流：[.github/workflows/deploy.yml](.github/workflows/deploy.yml)
- Caddy 配置模板：[deploy/Caddyfile](deploy/Caddyfile)

---

## 目录结构

```text
translated/         中文镜像（唯一真源），按官方 Path 镜像目录
  docs.json         导航与版本配置（迁移脚本据此生成侧边栏）
  docs/<版本>/**    文档正文（.mdx）
  specification/**  规范正文（.mdx）
  images/ logo/     静态资源
web/                Astro Starlight 工程
  astro.config.mjs  站点配置（GA4 / mermaid / 别名）
  src/              首页、自定义组件、生成内容（生成内容不入库）
scripts/            迁移脚本
deploy/             Caddyfile 模板
docs/               项目规则与流程文档（见下）
glossary.json       全局技术术语表
AGENTS.md           项目总纲与核心原则
```

---

## 翻译规范 / 项目文档

翻译任务前，**必须先阅读**以下文档并严格遵守：

| 文档 | 说明 |
|------|------|
| [AGENTS.md](AGENTS.md) | 项目总纲：目标、核心原则、重要限制、任务执行优先级 |
| [docs/translation-rules.md](docs/translation-rules.md) | 翻译规范：代码/API/术语/规范性语言/URL 的处理规则与最终检查清单 |
| [docs/workflow.md](docs/workflow.md) | 标准工作流：从发现源站到生成报告的 9 个阶段 |
| [docs/plan.md](docs/plan.md) | 分批执行规划：批次划分（B0–B9）、子批顺序与进度追踪 |
| [docs/本地预览.md](docs/本地预览.md) | 本地预览：迁移脚本 + Starlight 开发服务器 |
| [docs/部署.md](docs/部署.md) | 部署到 RackNerd 服务器（Caddy + GitHub Actions）|
| [glossary.json](glossary.json) | 全局术语表：确定后全站统一使用 |

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
