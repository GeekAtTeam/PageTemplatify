# PageTemplatify

✨ 简单灵活的静态 HTML 页面生成工具，基于 JSON 配置和 Jinja2 模板引擎，支持多主题多模板，适合企业官网、SaaS 平台、电商平台、个人博客、新闻网站等场景。

> Generate customizable static HTML pages using JSON configs and Jinja2 templates. Ideal for landing pages, company sites, SaaS platforms, e-commerce, blogs, and news websites.



## 🔧 项目特点

- 🧱 **配置驱动**：只需编辑 JSON 配置文件，无需编写代码；
- 🎨 **多主题风格**：内置 5 种专业模板，一套内容可切换多种风格；
- 🚀 **纯静态输出**：生成纯静态 HTML 文件，可部署于任何服务器或 CDN；
- 📦 **一键打包**：自动打包成 zip 文件，方便部署；
- 🐍 **Python + Jinja2**：依赖少，易用快速，跨平台兼容；
- 🌐 **适合备案用途**：支持展示备案信息与企业简介，适合 HTTP 服务验证；
- 💡 **易于扩展**：模板结构清晰，可自由定制样式和内容。



## 📦 安装依赖

```bash
git clone https://github.com/your-username/PageTemplatify.git
cd PageTemplatify
pip install -r requirements.txt
```



## 🚀 快速使用

### 查看支持的主题

列出所有可用的主题：
```bash
python ptfy.py list
```

### 基础用法

生成页面（使用默认配置）：
```bash
python ptfy.py build --theme enterprise
```

预览页面（支持热更新）：
```bash
python ptfy.py preview --theme enterprise
```

### 自定义配置

使用自定义配置文件：
```bash
python ptfy.py build --theme enterprise --config configs/my-config.json
python ptfy.py preview --theme enterprise --config configs/my-config.json
```



## 🎨 内置主题

PageTemplatify 内置了 5 种专业模板：

| 主题 | 适用场景 | 默认配置 |
|------|----------|----------|
| `enterprise` | 企业官网 | `configs/enterprise.json` |
| `saas` | SaaS 平台 | `configs/saas.json` |
| `ecommerce` | 电商平台 | `configs/ecommerce.json` |
| `blog` | 个人博客 | `configs/blog.json` |
| `news` | 新闻网站 | `configs/news.json` |



## 📁 目录结构

```bash
PageTemplatify/
├── configs/                # 内容配置文件（JSON）
│   ├── enterprise.json     # 企业官网配置
│   ├── saas.json          # SaaS 平台配置
│   ├── ecommerce.json     # 电商平台配置
│   ├── blog.json          # 个人博客配置
│   └── news.json          # 新闻网站配置
├── themes/                 # 主题模板（Jinja2 模板）
│   ├── enterprise/        # 企业官网模板
│   ├── saas/             # SaaS 平台模板
│   ├── ecommerce/        # 电商平台模板
│   ├── blog/             # 个人博客模板
│   └── news/             # 新闻网站模板
├── public/                 # 公共资源，如 CSS、图片
├── dist/                   # 输出目录（构建后 HTML）
├── ptfy.py                 # 生成脚本（命令行工具）
├── requirements.txt        # 依赖列表
└── README.md
```



## 📄 配置示例

### 企业官网配置（configs/enterprise.json）

```json
{
  "site_name": "广州极客艾特计算机系统有限公司",
  "hero_title": "极客艾特 Geek@",
  "hero_subtitle": "企业信息化解决方案专家",
  "description": "我们为客户提供一站式 IT 服务...",
  "carousel_title": "我们的服务场景",
  "carousel": [
    "carousel-1.webp",
    "carousel-2.webp",
    "carousel-3.webp"
  ],
  "about_title": "关于我们",
  "about_subtitle": "专业团队，值得信赖",
  "about_us": "成立于2025年，我们是一家专注于...",
  "about_features": [
    {
      "icon": "bi-award-fill",
      "title": "专业认证",
      "description": "获得多项行业认证，技术实力得到权威认可"
    }
  ],
  "services_title": "核心服务",
  "services_subtitle": "为您提供全方位的技术解决方案",
  "services": [
    {
      "name": "服务器运维",
      "icon": "bi-server",
      "description": "7×24小时专业运维服务，确保系统稳定运行"
    }
  ],
  "contact_title": "联系我们",
  "contact_subtitle": "随时为您提供专业服务",
  "contact": {
    "address": "广州市小蛮腰科技园G栋101室",
    "phone": "020-12345678",
    "email": "contact@geekat.cn",
    "work_time": "周一至周五 9:00-18:00",
    "icp": "粤ICP备20250000号",
    "police": "粤公网安备110105000000号"
  },
  "footer": {
    "copyright": "© 2024 广州极客艾特计算机系统有限公司. 保留所有权利。",
    "description": "专注于企业信息化解决方案，助力企业数字化转型"
  }
}
```



## 🎨 主题定制

你可以在 `themes/` 目录中自定义模板：

- 每个主题目录包含 `template.html` 文件
- 使用 Jinja2 模板语法
- 支持 Bootstrap 5 和 Bootstrap Icons
- 响应式设计，移动端友好



## 📦 部署说明

### 自动打包

构建完成后会自动生成 zip 文件：
```bash
python ptfy.py build --theme enterprise
# 输出：enterprise-enterprise.zip
```

### 手动部署

1. 构建页面：`python ptfy.py build --theme enterprise`
2. 将 `dist/` 目录内容上传到服务器
3. 配置 Web 服务器（Nginx、Apache 等）

### 快速部署

```bash
# 构建并打包
python ptfy.py build --theme enterprise

# 上传到服务器
scp enterprise-enterprise.zip user@server:/var/www/html/

# 在服务器上解压
ssh user@server "cd /var/www/html && unzip enterprise-enterprise.zip"
```



## 📄 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。



## 🙋‍♂️ 作者

由 [GeekAt 团队](https://geekat.cn) 维护，欢迎交流与合作！
