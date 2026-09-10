# 技术文档镜像工作流

## 总体流程

```text
官方文档
   ↓
阶段 1：发现
   ↓
阶段 2：分析
   ↓
阶段 3：建立 Sitemap
   ↓
阶段 4：建立 URL 映射
   ↓
阶段 5：建立术语表
   ↓
阶段 6：翻译
   ↓
阶段 7：Source / Target 对照
   ↓
阶段 8：保存
   ↓
阶段 9：生成报告
```

---

# 阶段 1：发现源网站

首先访问用户提供的官方文档地址。

获取：

* 网站名称
* 文档名称
* 文档版本
* 页面 URL
* 页面标题
* 页面层级
* Parent Page
* Child Page
* 内部链接
* 外部链接

此阶段：

> **不要翻译。**

---

# 阶段 2：分析网站结构

分析整个文档网站的导航结构。

建立：

```text
网站
├── 分类
│   ├── 页面
│   ├── 页面
│   └── 页面
│
└── 分类
    ├── 页面
    └── 页面
```

确认：

* 页面数量
* 页面层级
* 页面之间的关系
* 版本关系

---

# 阶段 3：建立 Sitemap

创建：

```text
source/sitemap.json
```

建议结构：

```json
{
  "url": "/docs/getting-started/intro",
  "title": "Introduction",
  "version": "v1",
  "parent": "/docs/getting-started",
  "children": []
}
```

每个页面必须有唯一记录。

---

# 阶段 4：建立 URL 映射

建立：

```text
source URL
      ↓
Chinese URL
```

例如：

```text
官方：

/docs/getting-started/intro

中文：

/docs/getting-started/intro
```

原则：

> 保持官方 Path，不重新设计 URL。

---

# 阶段 5：建立术语表

从官方文档中提取技术术语。

建立：

```text
docs/glossary.json
```

例如：

```json
{
  "authentication": "身份认证",
  "authorization": "授权",
  "endpoint": "端点",
  "request": "请求",
  "response": "响应"
}
```

术语一旦确定：

> 后续页面必须统一使用。

---

# 阶段 6：逐页面翻译

以页面为最小工作单位。

每个页面按照：

```text
读取官方页面
       ↓
分析结构
       ↓
翻译
       ↓
检查术语
       ↓
检查技术内容
       ↓
保存
```

执行。

不要一次性把大量页面混在一起翻译。

---

# 阶段 7：Source / Target 对照

每完成一个页面，立即进行源文档与中文文档对照。

检查：

```text
标题
Heading
段落
列表
表格
代码
API
参数
URL
链接
Note
Warning
数字
版本
技术术语
```

发现问题立即修正。

---

# 阶段 8：保存

中文页面使用与官方一致的 URL Path。

例如：

```text
source:

/docs/api/authentication

target:

/docs/api/authentication
```

同时保存页面元数据：

```json
{
  "sourceUrl": "https://example.com/docs/api/authentication",
  "sourceTitle": "Authentication",
  "sourcePath": "/docs/api/authentication",
  "sourceVersion": "v1",
  "lastSyncedAt": "2026-08-28"
}
```

---

# 阶段 9：最终报告

任务完成后输出：

```text
源网站：
页面总数：

发现页面：
已翻译：
已验证：
失败：
跳过：

术语数量：

Source / Target 差异：

失败页面：
```

同时列出：

```text
官方 URL
→
中文 URL
```

的映射关系。

---

# 网站更新流程

当官方文档更新时：

```text
重新获取 Sitemap
       ↓
与旧 Sitemap 比较
       ↓
识别新增页面
       ↓
识别删除页面
       ↓
识别修改页面
       ↓
只处理发生变化的页面
```

对于修改页面：

```text
官方旧版本
      ↓
官方新版本
      ↓
Diff
      ↓
确定变化区域
      ↓
重新翻译变化内容
      ↓
重新验证
```

不要无条件重新翻译整个网站。

---

# 失败处理

如果某个页面无法获取：

不要猜测内容。

记录：

```text
URL
失败原因
失败阶段
```

然后继续处理其他可以处理的页面。

最终报告中列出失败页面。

---

# 不确定内容处理

如果翻译过程中遇到无法确定的技术含义：

1. 查看当前页面上下文。
2. 查看同一网站相关页面。
3. 查看术语表。
4. 查看官方版本信息。
5. 如果仍无法确定，暂停该页面。
6. 报告具体问题。

禁止自行编造。

---

# 工作原则

始终保持：

```text
官方文档
    ↓
结构分析
    ↓
准确翻译
    ↓
逐页验证
    ↓
中文镜像
```

而不是：

```text
官方文档
    ↓
AI 总结
    ↓
AI 改写
    ↓
中文文章
```
