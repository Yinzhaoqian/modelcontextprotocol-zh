# 技术文档镜像 · 分批执行规划

> 源站：Model Context Protocol 官方文档（`https://modelcontextprotocol.io`）
> 范围：**全站 343 页**（docs 110 + specification 142 + 非版本化 91），**含 Draft**
> 原则：一个版本一个版本推进，**不一次性全量翻译**。每批独立跑通「阶段 5→9」并验收后再开下一批。

---

## 一、总体策略

1. **以「版本」为主批次**，版本内按「区域 / 子树」再分子批。
2. **latest（2026-07-28）优先**：它最新、访问量最大，且用于**首次建立术语表**（`glossary.json`）作为全局基线。
3. **越旧的发布版优先级越低**；**Draft 放最后**（内容随官方开发持续变动，最后同步以减少返工）。
4. **版本间复用**：新版本完成后，旧版本同名页面（路径相同、内容高度重叠）先做 **source diff**，只重译差异部分，复用已翻译内容 —— 对应 workflow「网站更新流程」。
5. **术语表增量维护**：V1 建立基线，之后每批只做增量补充，保持全站统一。

---

## 交付形态：Mintlify 中文站（已确定）

- 官方站 = Mintlify 渲染的 `.mdx` 源 + `docs.json`。中文镜像采用**同款 Mintlify**，观感与官方一致。
- **数据底本**：GitHub 原始 `.mdx`（`modelcontextprotocol/modelcontextprotocol` 仓库 `docs/` 下），带 frontmatter、相对资源路径；**不再用 `.md` 渲染端点**（那是产物，含注入块、CDN 图片）。
- **项目根 = `translated/`**：`translated/docs.json`（本地化中文导航）+ `translated/docs/<版本>/**.mdx` + `translated/images|logo|favicon.svg`（静态资源）。
- **每页产物 = `.mdx`**：frontmatter 的 `title`/`sidebarTitle`/`description` 翻译，其余键（`type`/`weight` 等）原样；正文不重复 H1（Mintlify 用 frontmatter title）。
- **镜像同步元数据**（sourceUrl/lastmod/lastSyncedAt）统一记录在 `sources/sitemap.json`，不写入 `.mdx`。
- **本地预览**：`cd translated && npx mint dev` → `http://localhost:3000`。
- 每完成一页：写 `.mdx` + 下载该页图片 + 在 `docs.json` 导航加入该页（中文 group 名）。

---

## 二、目录约定

```text
sources/           官方原始数据（sitemap.xml / llms.txt / sitemap.json / url-mapping.json）
translated/        中文镜像，按官方 Path 镜像目录
  docs/<版本>/...
  specification/<版本>/...
  community/... registry/... extensions/... seps/...
docs/glossary.json 全局术语表（阶段 5 建立，持续增量）
```

每个中文页面保存时附带元数据（sourceUrl / sourceTitle / sourcePath / sourceVersion / lastmod / lastSyncedAt），遵循 workflow 阶段 8。

---

## 三、批次划分与顺序

| 批次 | 范围 | 页数 | 依赖 | 说明 |
|---|---|---|---|---|
| **B0** | 分析 / Sitemap / URL 映射 / 统计 | — | — | ✅ 已完成（阶段 1–4） |
| **B1** | `docs/2026-07-28`（latest 文档） | 23 | B0 | 跑通完整流程 + **首建 glossary.json** |
| **B2** | `specification/2026-07-28`（latest 规范） | 31 | B1 | 术语最密集，扩充 glossary |
| **B3** | `docs/2025-11-25` + `specification/2025-11-25` | 38 | B2（diff 复用） | 与 latest diff，只译差异 |
| **B4** | `docs/2025-06-18` + `specification/2025-06-18` | 37 | B3 | 同上 |
| **B5** | `docs/2025-03-26` + `specification/2025-03-26` | 35 | B4 | 同上 |
| **B6** | `docs/2024-11-05` + `specification/2024-11-05` | 34 | B5 | 同上 |
| **B7** | 非版本化：community 28 · registry 11 · extensions 8 · development 1 · examples 1 | 49 | — | 与版本无关，可插空进行 |
| **B8** | `seps`（Specification Enhancement Proposals） | 42 | — | 提案文档，独立成批 |
| **B9** | `docs/draft` + `specification/draft` | 54 | 全部之后 | **最后做**，易变，最终同步 |

> 合计 343 页。latest 两批（B1+B2）= 54 页，先把它完整交付，形成可用的中文镜像最小闭环。

---

## 四、版本内子批（避免单批过大）

**B1 · docs/2026-07-28（23 页）** 建议顺序：
1. `getting-started/intro`（1）
2. `learn/*`（architecture, server-concepts, client-concepts, versioning — 4）
3. `develop/*`（connect-local/remote-servers, build-with-agent-skills, build-server, build-client, clients/client-best-practices — 6）
4. `sdk`（1）
5. `tutorials/security/*`（authorization, security_best_practices — 2）
6. `tools/*`（inspector index + 7 子页 + debugging — 9）

**B2 · specification/2026-07-28（31 页）** 建议顺序：
1. `index` / `changelog` / `deprecated` / `architecture` / `schema`
2. `basic/*`（含 versioning、patterns/*、transports/*、authorization/*）
3. `client/*`（roots, sampling, elicitation）
4. `server/*`（discover, prompts, resources, tools, utilities/*）

其余版本子批同构，按同名子树推进。

---

## 五、单批内工作流（每批必做，来自 workflow 阶段 5–9）

```text
读取官方 .md 原文  →  分析结构  →  翻译  →  查术语表  →  查技术内容
        →  Source/Target 对照（阶段 7 清单）  →  修正  →  保存 + 元数据
```

批次收尾：更新术语表、更新本文件进度表、输出该批小结（已译 / 已验证 / 失败 / 跳过）。

---

## 六、进度追踪

| 批次 | 状态 | 已译 | 已验证 | 失败 | 备注 |
|---|---|---|---|---|---|
| B0 分析 | ✅ 完成 | — | — | — | sitemap.json / url-mapping.json 就绪 |
| B1 docs/2026-07-28 | ✅ 完成 | 23/23 | 23 | 0 | 全部入站；Mintlify 中文站可浏览（localhost:3000） |
| B2 spec/2026-07-28 | ✅ 完成 | 31/31 | 31 | 0 | 全部入站；「规范」tab 已上线（schema.mdx 为自动生成类型参考，按代码原样保留） |
| B3 2025-11-25 | ✅ 完成 | 38/38 | 38 | 0 | 文档 16/16 + 规范 22/22（schema 原样保留）全部入站；「文档」「规范」两个 tab 均加「版本 2025-11-25」下拉；localhost:3000 全部 200，编译无错 |
| B4 2025-06-18 | ⬜ 未开始 | 0/37 | 0 | 0 | diff 复用 |
| B5 2025-03-26 | ⬜ 未开始 | 0/35 | 0 | 0 | diff 复用 |
| B6 2024-11-05 | ⬜ 未开始 | 0/34 | 0 | 0 | diff 复用 |
| B7 非版本化 | ✅ 完成 | 49/49 | 49 | 0 | 全部入站；新增「扩展」「注册表」「社区」三个 tab；图片(4 gif + ecosystem svg)已下齐，localhost:3000 可浏览 |
| B8 seps | ✅ 完成 | 42/42 | 42 | 0 | 全部入站；新增「SEPs」tab（41 篇提案 + 总览 index）；含 mermaid/GitHub alert/长规范表；localhost:3000 全部 200 |
| B9 draft | ⬜ 未开始 | 0/54 | 0 | 0 | 最后同步 |

图例：⬜ 未开始 · 🟡 进行中 · ✅ 完成

---

## 七、验收口径（每批结束）

- 结构一致：标题 / Heading 层级 / 列表 / 表格 / 代码块与官方一致
- 技术零改动：API、参数、JSON 字段、HTTP Header、错误码、版本号、数字保持原样
- 规范性语言（MUST/SHOULD/MAY）强度未变
- 术语与 `glossary.json` 一致
- URL：内链映射到镜像对应页，外链保持原址
- 元数据齐全，可回溯官方源页与同步时间
