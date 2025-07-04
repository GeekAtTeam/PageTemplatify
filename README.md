# PageTemplatify

✨ 简单灵活的静态 HTML 页面生成工具，基于 JSON 配置和 Jinja2 模板引擎，支持多主题多模板，适合企业官网、备案展示页、SaaS 落地页、电商宣传页等场景。

> Generate customizable static HTML pages using JSON configs and Jinja2 templates. Ideal for landing pages, company sites, or ICP-ready pages.



## 🔧 项目特点

- 🧱 **配置驱动**：只需编辑 JSON 配置文件，无需编写代码；
- 🎨 **多主题风格**：一套内容可切换多种配色与布局模板；
- 📦 **纯静态输出**：生成纯静态 HTML 文件，可部署于任何服务器或 CDN；
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

生成页面：

```bash
python ptfy.py --config configs/enterprise.json --theme default
```

生成的 HTML 文件会输出到 `dist/enterprise-default.html`。



## 📁 目录结构

```bash
PageTemplatify/
├── configs/                # 内容配置文件（JSON / YAML）
│   ├── enterprise.json
│   ├── saas.json
│   └── ecommerce.json
├── themes/                 # 主题模板（Jinja2 模板文件夹）
│   ├── default/
│   ├── minimal/
│   └── ecommerce/
├── public/                 # 公共资源，如 CSS、图片
├── dist/                   # 输出目录（构建后 HTML）
├── ptfy.py                 # 生成脚本（命令行工具）
├── requirements.txt        # 依赖列表（Jinja2）
└── README.md
```



## 📄 配置示例（configs/enterprise.json）

```json
{
  "site_name": "某某公司",
  "slogan": "企业信息化解决方案专家",
  "description": "我们为客户提供一站式 IT 服务，包括服务器运维、备案咨询、安全防护等。",
  "carousel": [
    "https://picsum.photos/800/300?random=1",
    "https://picsum.photos/800/300?random=2"
  ],
  "about_us": "成立于2020年，服务全国300+企业客户。",
  "services": ["服务器运维", "系统监控", "安全加固", "ICP备案"],
  "contact": {
    "address": "北京市中关村科技园",
    "phone": "010-12345678",
    "icp": "京ICP备20250000号",
    "police": "京公网安备110105000000号"
  }
}
```



## 🎨 主题支持

你可以在 `themes/` 目录中自定义模板：

- `default/`：商务蓝色风格
- `minimal/`：极简黑白风格
- `ecommerce/`：红色电商风格



## 📄 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。



## 🙋‍♂️ 作者

由 [GeekAt 团队](https://geekat.cn) 维护，欢迎交流与合作！
