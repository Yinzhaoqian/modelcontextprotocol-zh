// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sidebar from './src/sidebar.generated.mjs';
import { remarkMermaid } from './remark-mermaid.mjs';

// 站点正式域名（部署到 RackNerd 后替换为真实域名）
const SITE = 'https://example.com';
const GA4_ID = 'G-6NZJWQG9XZ';

export default defineConfig({
  site: SITE,
  integrations: [
    starlight({
      title: '模型上下文协议',
      defaultLocale: 'root',
      locales: {
        root: { label: '简体中文', lang: 'zh-CN' },
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/modelcontextprotocol' },
      ],
      // Google Analytics 4
      head: [
        {
          tag: 'script',
          attrs: { async: true, src: `https://www.googletagmanager.com/gtag/js?id=${GA4_ID}` },
        },
        {
          tag: 'script',
          content: `window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','${GA4_ID}');`,
        },
        // 客户端 mermaid 渲染
        { tag: 'script', attrs: { type: 'module', src: '/mermaid-init.js' } },
      ],
      // 侧边栏：迁移脚本生成 ./src/sidebar.generated.mjs
      sidebar,
    }),
  ],
  markdown: {
    remarkPlugins: [remarkMermaid],
  },
  vite: {
    resolve: {
      alias: {
        '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
      },
    },
  },
});
