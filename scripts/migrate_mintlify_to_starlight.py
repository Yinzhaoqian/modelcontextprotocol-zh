# -*- coding: utf-8 -*-
"""
将 translated/ 下的 Mintlify .mdx 迁移为 Starlight 内容。
- 转换 Mintlify 专有组件为 Starlight 语法 / 自定义组件
- 保护代码块（围栏 + 行内），避免误伤代码里的泛型/XML
- 复制静态资源（images / logo）到 web/public
- 解析 docs.json 生成 Starlight 侧边栏 web/src/sidebar.generated.mjs
"""
import json
import posixpath
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "translated"
DST = ROOT / "web" / "src" / "content" / "docs"
PUBLIC = ROOT / "web" / "public"

# 需要复制的静态资源目录
ASSET_DIRS = ["images", "logo"]

# 顶层内容目录/文件（index.mdx 由 Starlight 首页替代，跳过）
SKIP_FILES = {"index.mdx"}

FENCE_RE = re.compile(r"(^|\n)([ \t]*)(`{3,}|~{3,})")


def split_frontmatter(text):
    if text.startswith("---"):
        m = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
        if m:
            return m.group(1), text[m.end():]
    return None, text


def parse_frontmatter(fm):
    """极简 YAML：只取顶层 key: value（值可带引号）。"""
    data = {}
    if not fm:
        return data
    for line in fm.splitlines():
        m = re.match(r'^([A-Za-z0-9_-]+):\s*(.*)$', line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if len(v) >= 2 and ((v[0] == v[-1] == '"') or (v[0] == v[-1] == "'")):
                v = v[1:-1]
            data[k] = v
    return data


def yaml_escape(v):
    v = str(v).replace('\\', '\\\\').replace('"', '\\"')
    return f'"{v}"'


def mask_code(body):
    """把围栏代码块与行内代码替换为占位符，返回 (masked, store)。"""
    store = []

    # 围栏代码块
    lines = body.split("\n")
    out = []
    i = 0
    fence = None
    buf = []
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()
        m = re.match(r'(`{3,}|~{3,})', stripped)
        if fence is None and m:
            fence = m.group(1)[0] * len(m.group(1))
            buf = [line]
            i += 1
            continue
        if fence is not None:
            buf.append(line)
            if re.match(r'(`{3,}|~{3,})\s*$', stripped) and stripped[0] == fence[0] and len(re.match(r'(`{3,}|~{3,})', stripped).group(1)) >= len(fence):
                token = f"⟦CODEBLOCK{len(store)}⟧"
                store.append("\n".join(buf))
                out.append(token)
                fence = None
                buf = []
            i += 1
            continue
        out.append(line)
        i += 1
    if fence is not None:  # 未闭合，原样放回
        out.extend(buf)
    masked = "\n".join(out)

    # 行内代码 `...`
    def repl_inline(mm):
        token = f"⟦INLINE{len(store)}⟧"
        store.append(mm.group(0))
        return token
    masked = re.sub(r'`[^`\n]+`', repl_inline, masked)

    return masked, store


def unmask_code(text, store):
    # 先还原行内，再还原围栏（占位符互不重叠，顺序无所谓，统一还原）
    for idx in range(len(store) - 1, -1, -1):
        text = text.replace(f"⟦INLINE{idx}⟧", store[idx])
        text = text.replace(f"⟦CODEBLOCK{idx}⟧", store[idx])
    return text


def get_attr(tag, name):
    m = re.search(name + r'\s*=\s*"([^"]*)"', tag)
    if m:
        return m.group(1)
    m = re.search(name + r"\s*=\s*'([^']*)'", tag)
    if m:
        return m.group(1)
    m = re.search(name + r'\s*=\s*\{([^}]*)\}', tag)
    if m:
        return m.group(1).strip().strip('"').strip("'")
    return None


def inner_to_desc(inner):
    txt = re.sub(r'\s+', ' ', inner).strip()
    txt = txt.replace('"', "'")
    return txt


ASIDE_MAP = {
    'Note': 'note', 'Info': 'note', 'Tip': 'tip', 'Check': 'tip',
    'Warning': 'caution', 'Caution': 'caution', 'Danger': 'danger', 'Important': 'caution',
}


def transform(body, used):
    # --- Frame：去壳保留内部 ---
    body = re.sub(r'<Frame\b[^>]*>', '', body)
    body = body.replace('</Frame>', '')

    # --- CodeGroup：去壳，内部代码块（已被 mask）保留 ---
    body = re.sub(r'<CodeGroup\b[^>]*>', '', body)
    body = body.replace('</CodeGroup>', '')

    # --- AccordionGroup：去壳 ---
    body = re.sub(r'<AccordionGroup\b[^>]*>', '', body)
    body = body.replace('</AccordionGroup>', '')

    # --- Accordion -> details/summary ---
    def repl_acc(m):
        title = get_attr(m.group(0), 'title') or '详情'
        inner = m.group(1)
        return f"<details>\n<summary>{title}</summary>\n\n{inner}\n\n</details>"
    body = re.sub(r'<Accordion\b[^>]*>(.*?)</Accordion>', repl_acc, body, flags=re.DOTALL)

    # --- CardGroup -> CardGrid ---
    if re.search(r'<CardGroup\b', body):
        used.add('CardGrid')
    body = re.sub(r'<CardGroup\b[^>]*>', '<CardGrid>', body)
    body = body.replace('</CardGroup>', '</CardGrid>')

    # --- Card（带内容） ---
    def repl_card(m):
        tag = m.group(0)
        inner = m.group(1)
        title = get_attr(tag, 'title') or ''
        href = get_attr(tag, 'href')
        if href:
            used.add('LinkCard')
            desc = inner_to_desc(inner)
            if not title:
                title = desc[:30]
            attrs = f'title="{title}" href="{href}"'
            if desc:
                attrs += f' description="{desc}"'
            return f'<LinkCard {attrs} />'
        else:
            used.add('Card')
            return f'<Card title="{title}">{inner}</Card>'
    body = re.sub(r'<Card\b[^>]*?>(.*?)</Card>', repl_card, body, flags=re.DOTALL)

    # --- Card（自闭合） ---
    def repl_card_self(m):
        tag = m.group(0)
        title = get_attr(tag, 'title') or ''
        href = get_attr(tag, 'href')
        if href:
            used.add('LinkCard')
            return f'<LinkCard title="{title}" href="{href}" />'
        used.add('Card')
        return f'<Card title="{title}"></Card>'
    body = re.sub(r'<Card\b[^>]*/>', repl_card_self, body)

    # --- Tabs / Tab -> Tabs / TabItem ---
    if re.search(r'<Tabs\b', body):
        used.add('Tabs'); used.add('TabItem')

    def repl_tab(m):
        tag = m.group(0)
        label = get_attr(tag, 'title') or get_attr(tag, 'label') or ''
        return f'<TabItem label="{label}">'
    body = re.sub(r'<Tab\b[^>]*>', repl_tab, body)
    body = body.replace('</Tab>', '</TabItem>')
    # 修正：上一步把 </Tabs> 也替换成了 </TabItem>s？不会，因 </Tab> 精确匹配。但 <Tabs> 被 repl_tab 命中！修正下面
    # （<Tabs> 会匹配 <Tab\b...> 吗？\b 后是 's'，是单词字符，\b 不在此处断开 -> 不匹配。安全。）

    # --- Steps / Step -> 自定义组件 ---
    if re.search(r'<Steps\b', body):
        used.add('Steps'); used.add('Step')

    def repl_step(m):
        tag = m.group(0)
        title = get_attr(tag, 'title')
        return f'<Step title="{title}">' if title else '<Step>'
    body = re.sub(r'<Step\b[^>]*>', repl_step, body)

    # --- Icon：移除 ---
    body = re.sub(r'<Icon\b[^>]*/>', '', body)
    body = re.sub(r'<Icon\b[^>]*>.*?</Icon>', '', body, flags=re.DOTALL)

    # --- Badge / Tooltip：保留文本去壳 ---
    body = re.sub(r'<Badge\b[^>]*>(.*?)</Badge>', r'\1', body, flags=re.DOTALL)
    body = re.sub(r'<Tooltip\b[^>]*>(.*?)</Tooltip>', r'\1', body, flags=re.DOTALL)

    # --- Tree -> 文本文件树代码块 ---
    def repl_tree(m):
        inner = m.group(1)
        out_lines = []
        for line in inner.split('\n'):
            indent = line[:len(line) - len(line.lstrip())]
            s = line.strip()
            if not s:
                continue
            fm = re.match(r'<Tree\.Folder\b(.*?)/?>', s)
            ff = re.match(r'<Tree\.File\b(.*?)/?>', s)
            if fm:
                name = get_attr(s, 'name') or ''
                out_lines.append(f"{indent}{name}/")
            elif ff:
                name = get_attr(s, 'name') or ''
                comment = get_attr(s, 'comment')
                out_lines.append(f"{indent}{name}" + (f"    # {comment}" if comment else ''))
            # 忽略 </Tree.Folder> 等闭合标签
        return "```text\n" + "\n".join(out_lines) + "\n```"
    body = re.sub(r'<Tree\b[^>]*>(.*?)</Tree>', repl_tree, body, flags=re.DOTALL)

    # --- Asides：<Note>...</Note> -> :::note ... ::: ---
    for comp, kind in ASIDE_MAP.items():
        body = re.sub(rf'<{comp}\b[^>]*>', f'\n:::{kind}\n', body)
        body = re.sub(rf'</{comp}>', '\n:::\n', body)

    return body


def build_imports(used):
    lines = []
    sl = [c for c in ['Card', 'CardGrid', 'LinkCard', 'Tabs', 'TabItem'] if c in used]
    if sl:
        lines.append("import { " + ", ".join(sl) + " } from '@astrojs/starlight/components';")
    if 'Steps' in used:
        lines.append("import Steps from '@components/Steps.astro';")
        lines.append("import Step from '@components/Step.astro';")
    return "\n".join(lines)


def rewrite_assets(text, rel: Path):
    base = '' if rel.parent == Path('.') else rel.parent.as_posix()

    def to_abs(p):
        if p.startswith(('/', 'http://', 'https://', '#', 'mailto:', 'data:')):
            return p
        if p.startswith(('./', '../')):
            joined = (base + '/' + p) if base else p
            return '/' + posixpath.normpath(joined)
        return p

    text = re.sub(r'(src=")([^"]+)(")', lambda m: m.group(1) + to_abs(m.group(2)) + m.group(3), text)
    text = re.sub(r"(src=')([^']+)(')", lambda m: m.group(1) + to_abs(m.group(2)) + m.group(3), text)
    text = re.sub(r'(!\[[^\]]*\]\()([^)\s]+)(\))', lambda m: m.group(1) + to_abs(m.group(2)) + m.group(3), text)
    return text


def convert_file(src_path: Path, rel: Path):
    raw = src_path.read_text(encoding="utf-8")
    fm_raw, body = split_frontmatter(raw)
    fm = parse_frontmatter(fm_raw)

    # 移除源里的 import（Mintlify snippet 引用，路径不存在）
    body = re.sub(r'(?m)^import\s+.*$', '', body)

    masked, store = mask_code(body)
    used = set()
    masked = transform(masked, used)
    masked = rewrite_assets(masked, rel)
    body = unmask_code(masked, store)

    imports = build_imports(used)

    # 新 frontmatter
    title = fm.get('title') or src_path.stem
    out_fm = ['---', f'title: {yaml_escape(title)}']
    if fm.get('description'):
        out_fm.append(f'description: {yaml_escape(fm["description"])}')
    if fm.get('sidebarTitle'):
        out_fm.append('sidebar:')
        out_fm.append(f'  label: {yaml_escape(fm["sidebarTitle"])}')
    out_fm.append('---')

    parts = ["\n".join(out_fm), ""]
    if imports:
        parts.append(imports)
        parts.append("")
    parts.append(body.strip() + "\n")
    out = "\n".join(parts)

    dst_path = (DST / rel).with_suffix(".mdx")
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_path.write_text(out, encoding="utf-8")


# ---------------- 侧边栏 ----------------

def slug_of(page):
    s = page.lower()
    if s.endswith('/index'):
        s = s[:-len('/index')]
    return s


def build_pages(pages):
    items = []
    for p in pages:
        if isinstance(p, str):
            items.append({"slug": slug_of(p)})
        elif isinstance(p, dict) and 'group' in p:
            items.append({
                "label": p['group'],
                "collapsed": True,
                "items": build_pages(p.get('pages', [])),
            })
    return items


def build_sidebar(docs_json):
    tabs = docs_json.get('navigation', {}).get('tabs', [])
    sidebar = []
    for tab in tabs:
        group = {"label": tab['tab'], "items": []}
        if 'versions' in tab:
            for v in tab['versions']:
                group['items'].append({
                    "label": v['version'],
                    "collapsed": not v.get('default', False),
                    "items": build_pages(v.get('pages', [])),
                })
        else:
            group['items'] = build_pages(tab.get('pages', []))
        sidebar.append(group)
    return sidebar


def main():
    # 清空旧内容（保留 index.mdx 首页）
    if DST.exists():
        for child in DST.iterdir():
            if child.name == 'index.mdx':
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

    count = 0
    for src_path in SRC.rglob("*.mdx"):
        rel = src_path.relative_to(SRC)
        if str(rel) in SKIP_FILES or rel.name in SKIP_FILES and len(rel.parts) == 1:
            continue
        if rel.parts[0] == 'mdx':  # 官方原始英文数据，跳过
            continue
        convert_file(src_path, rel)
        count += 1

    # 复制静态资源：translated 下所有非 mdx/json 文件，按原相对路径 -> public/
    assets = 0
    for f in SRC.rglob("*"):
        if f.is_dir():
            continue
        if f.suffix.lower() in ('.mdx', '.json'):
            continue
        rel = f.relative_to(SRC)
        out = PUBLIC / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out)
        assets += 1

    # 侧边栏
    docs_json = json.loads((SRC / "docs.json").read_text(encoding="utf-8"))
    sidebar = build_sidebar(docs_json)
    sb_out = ("// 该文件由 scripts/migrate_mintlify_to_starlight.py 生成，请勿手动编辑。\n"
              "export default " + json.dumps(sidebar, ensure_ascii=False, indent=2) + ";\n")
    (ROOT / "web" / "src" / "sidebar.generated.mjs").write_text(sb_out, encoding="utf-8")

    print(f"converted {count} pages; sidebar groups: {len(sidebar)}")


if __name__ == "__main__":
    main()
