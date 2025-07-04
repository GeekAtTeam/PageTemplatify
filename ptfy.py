#!/usr/bin/env python3
import os
import sys
import json
import argparse
from jinja2 import Environment, FileSystemLoader
import http.server
import socketserver

def build(args):
    config_path = os.path.abspath(args.config)
    if not os.path.isfile(config_path):
        print(f"错误：配置文件不存在: {config_path}")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"错误：JSON 格式错误 - {e}")
            sys.exit(1)

    theme_name = args.theme
    theme_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'themes', theme_name)
    template_file = 'template.html'

    if not os.path.isdir(theme_dir):
        print(f"错误：主题目录不存在: {theme_dir}")
        sys.exit(1)

    env = Environment(loader=FileSystemLoader(theme_dir))
    try:
        template = env.get_template(template_file)
    except Exception as e:
        print(f"错误：加载模板失败 - {e}")
        sys.exit(1)

    html = template.render(config)

    dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
    os.makedirs(dist_dir, exist_ok=True)

    config_name = os.path.splitext(os.path.basename(config_path))[0]
    # output_path = os.path.join(dist_dir, f"{config_name}-{theme_name}.html")
    output_path = os.path.join(dist_dir, f"index.html")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 页面生成成功: {output_path}")

def preview(args):
    dist_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
    if not os.path.isdir(dist_dir):
        print(f"错误：dist 目录不存在，请先生成页面。")
        sys.exit(1)
    port = args.port
    os.chdir(dist_dir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🌐 本地预览服务已启动: http://localhost:{port}")
        print("按 Ctrl+C 停止服务。")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务已停止。")

def main():
    parser = argparse.ArgumentParser(description="PageTemplatify (ptfy) - 静态 HTML 页面生成器")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # build 子命令
    parser_build = subparsers.add_parser('build', help='生成静态页面')
    parser_build.add_argument('--config', '-c', required=True, help='JSON 配置文件路径')
    parser_build.add_argument('--theme', '-t', default='default', help='主题名称，默认 default')
    parser_build.set_defaults(func=build)

    # preview 子命令
    parser_preview = subparsers.add_parser('preview', help='本地预览 dist 目录')
    parser_preview.add_argument('--port', '-p', type=int, default=9469, help='预览服务端口，默认 9469')
    parser_preview.set_defaults(func=preview)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
