# 技术文档中文翻译规范

## 一、翻译目标

本项目的翻译目标是：

> 将官方技术文档准确、完整、专业地翻译成中文，同时保持与源文档的结构和技术语义一致。

翻译结果必须适合：

* 软件工程师
* AI 工程师
* 后端工程师
* 前端工程师
* DevOps 工程师
* 架构师
* 技术负责人

阅读。

---

# 二、基本原则

始终遵循：

> 翻译，而不是改写。

> 映射，而不是重新解释。

> 保留结构、保留语义、保证技术准确性。

---

# 三、完整性

必须尽可能完整保留：

* 标题
* H1
* H2
* H3
* H4
* Breadcrumb
* 页面目录
* 正文
* 列表
* 表格
* Note
* Tip
* Warning
* Important
* FAQ
* 图片
* 图片说明
* 示例
* 代码
* 页面导航

不得因为内容较长而删除内容。

---

# 四、代码

代码必须保持原样。

例如：

```java
Client client = new Client();
client.connect(server);
```

不得翻译：

```java
客户端 客户端 = new 客户端();
客户端.连接(服务器);
```

必须保持：

* 类名
* 方法名
* 变量名
* 参数名
* API
* 字段名
* 包名
* 模块名
* 文件名

不变。

---

# 五、代码注释

代码本身不能修改。

代码中的自然语言注释可以翻译。

例如：

```java
// Create a new client
Client client = new Client();
```

可以翻译成：

```java
// 创建一个新的客户端
Client client = new Client();
```

---

# 六、API 和协议字段

以下内容不得翻译：

```text
API 名称
API Endpoint
HTTP Method
HTTP Header
JSON Key
JSON-RPC Method
协议字段
错误码
参数名称
环境变量
CLI 参数
```

例如：

```text
tools/call
initialize
Authorization
Content-Type
Mcp-Protocol-Version
```

必须保持原样。

---

# 七、技术术语

技术术语不能机械逐词翻译。

应该综合：

* 官方术语
* 行业惯用表达
* 技术上下文
* 项目术语表

确定中文译法。

首次出现的专业术语可以使用：

```text
中文名称（English Term，缩写）
```

例如：

```text
模型上下文协议（Model Context Protocol，MCP）
```

后续保持统一。

---

# 八、行业标准术语

以下类型的术语通常保留英文：

```text
API
SDK
HTTP
HTTPS
OAuth
JSON
JSON-RPC
JWT
URL
URI
REST
GraphQL
WebSocket
SSE
Git
GitHub
Docker
Kubernetes
```

不要为了中文化而强行翻译。

---

# 九、规范性语言

协议和标准文档中的规范性语言必须准确翻译。

例如：

```text
MUST
→ 必须

MUST NOT
→ 不得

SHOULD
→ 应当

SHOULD NOT
→ 不应当

MAY
→ 可以

REQUIRED
→ 必需 / 必须

OPTIONAL
→ 可选
```

不得降低或提高原文要求的强度。

---

# 十、数字

数字必须与原文完全一致。

包括：

* 时间
* 数量
* 百分比
* 版本号
* 端口
* 超时时间
* 限制
* HTTP Status Code

例如：

```text
5 seconds
```

不能翻译成：

```text
几秒钟
```

应该保持：

```text
5 秒
```

---

# 十一、URL

URL 不得修改。

例如：

```text
https://example.com/docs/api
```

必须保持：

```text
https://example.com/docs/api
```

内部链接需要映射到中文镜像站对应页面。

外部链接保持原始地址。

---

# 十二、链接

内部链接：

```text
官方：

/docs/api/authentication

中文：

/docs/api/authentication
```

外部链接：

保持原始地址。

例如：

* GitHub
* IETF
* W3C
* RFC
* npm
* PyPI
* 官方项目网站

---

# 十三、表格

表格必须保持：

* 行
* 列
* 顺序
* 数据
* 字段

只翻译自然语言。

不要修改：

* 数字
* API 名称
* 字段名
* URL
* 错误码
* 版本号

---

# 十四、图片

保留：

* 图片
* 图片地址
* 图片标题
* 图片说明
* 图表
* 架构图

不要改变图片表达的技术含义。

---

# 十五、术语一致性

同一个英文术语在整个网站中必须保持一致。

例如：

```text
Authentication
→ 身份认证
```

不要在其他页面随意变成：

```text
身份验证
鉴权
认证机制
```

除非上下文存在明确的技术差异。

---

# 十六、禁止增加内容

默认情况下禁止增加：

* AI 总结
* AI 解释
* 个人观点
* 最佳实践
* 技术推测
* 额外教程
* 官方没有说明的信息

---

# 十七、禁止删除内容

不得删除：

* 技术限制
* 参数说明
* Warning
* Note
* API 示例
* 错误说明
* 安全说明
* 边界条件

---

# 十八、中文语言风格

中文应该：

* 专业
* 简洁
* 准确
* 自然
* 符合开发者阅读习惯

避免：

* 机械直译
* 过度书面化
* AI 腔
* 网络流行语
* 营销语言

---

# 十九、翻译优先级

始终遵循：

```text
技术准确性
    ↓
语义完整性
    ↓
上下文一致性
    ↓
术语一致性
    ↓
中文自然度
```

---

# 二十、最终检查

翻译完成后必须检查：

```text
[ ] 标题完整
[ ] Heading 层级一致
[ ] 正文完整
[ ] 列表完整
[ ] 表格完整
[ ] 代码完整
[ ] API 完整
[ ] 参数完整
[ ] URL 完整
[ ] 链接完整
[ ] Note 完整
[ ] Warning 完整
[ ] 数字一致
[ ] 版本一致
[ ] MUST / SHOULD / MAY 含义一致
[ ] 技术术语统一
[ ] 没有遗漏
[ ] 没有增加未经确认的信息
[ ] 没有改变技术含义
```
