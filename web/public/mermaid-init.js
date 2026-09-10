import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';

function currentTheme() {
  const t = document.documentElement.dataset.theme;
  return t === 'light' ? 'default' : 'dark';
}

function renderAll() {
  const blocks = document.querySelectorAll('pre.mermaid');
  if (!blocks.length) return;
  blocks.forEach((el) => {
    // 保存原始图定义，便于主题切换时重渲染
    if (!el.dataset.src) el.dataset.src = el.textContent;
    else {
      el.textContent = el.dataset.src;
      el.removeAttribute('data-processed');
    }
  });
  mermaid.initialize({ startOnLoad: false, theme: currentTheme(), securityLevel: 'loose' });
  try {
    mermaid.run({ nodes: blocks });
  } catch (e) {
    console.error('mermaid render error', e);
  }
}

// 首次加载 + Astro 客户端导航
document.addEventListener('DOMContentLoaded', renderAll);
document.addEventListener('astro:page-load', renderAll);
if (document.readyState !== 'loading') renderAll();

// 跟随明暗主题切换重渲染
const observer = new MutationObserver((muts) => {
  for (const m of muts) {
    if (m.attributeName === 'data-theme') {
      renderAll();
      break;
    }
  }
});
observer.observe(document.documentElement, { attributes: true });
