#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import argparse
from jinja2 import Environment, FileSystemLoader
import http.server
import socketserver
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time
import shutil
import zipfile

def build(args):
    # 获取脚本所在目录，确保路径正确
    root_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = args.config
    if not os.path.isabs(config_path):
        config_path = os.path.join(root_dir, config_path)
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
    theme_dir = os.path.join(root_dir, 'themes', theme_name)
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

    dist_dir = os.path.join(root_dir, 'dist')
    os.makedirs(dist_dir, exist_ok=True)

    # 复制 public 目录到 dist 目录
    public_dir = os.path.join(root_dir, 'public')
    if os.path.isdir(public_dir):
        # 直接复制 public 目录下的文件到 dist 目录
        for item in os.listdir(public_dir):
            src = os.path.join(public_dir, item)
            dst = os.path.join(dist_dir, item)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            elif os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
        print(f"✅ 已复制 public 资源到: {dist_dir}")

    output_path = os.path.join(dist_dir, f"index.html")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ 页面生成成功: {output_path}")

    # 打包 dist 目录为 zip 文件
    config_name = os.path.splitext(os.path.basename(config_path))[0]
    zip_filename = f"{config_name}-{theme_name}.zip"
    zip_path = os.path.join(root_dir, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # 在 zip 中创建多一级目录结构
                arcname = os.path.join(f"{config_name}-{theme_name}", os.path.relpath(file_path, dist_dir))
                zipf.write(file_path, arcname)
    
    print(f"📦 打包完成: {zip_path}")
    print(f"💡 提示：可以使用 scp {zip_filename} user@server:/path/to/upload/ 上传到服务器")
    print(f"📁 解压后会创建目录: {config_name}-{theme_name}/")

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, build_func, args):
        super().__init__()
        self.build_func = build_func
        self.args = args
        self.last_build = 0
        self.debounce_interval = 0.5  # 秒
    def on_any_event(self, event):
        if not event.is_directory:
            now = time.time()
            if now - self.last_build > self.debounce_interval:
                print("检测到文件变动，自动重新生成页面...")
                self.build_func(self.args)
                self.last_build = now

def preview(args):
    # 获取脚本所在目录，确保路径正确
    root_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(root_dir, 'dist')
    config_path = args.config
    if not os.path.isabs(config_path):
        config_path = os.path.join(root_dir, config_path)
    theme_name = args.theme
    theme_dir = os.path.join(root_dir, 'themes', theme_name)
    if not os.path.isfile(config_path):
        print(f"错误：配置文件不存在: {config_path}")
        sys.exit(1)
    if not os.path.isdir(theme_dir):
        print(f"错误：主题目录不存在: {theme_dir}")
        sys.exit(1)
    # 启动时先生成一次
    build(args)
    # 启动文件监听
    event_handler = ReloadHandler(build, args)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(config_path), recursive=False)
    observer.schedule(event_handler, path=theme_dir, recursive=True)
    observer_thread = threading.Thread(target=observer.start)
    observer_thread.daemon = True
    observer_thread.start()
    print(f"🔄 已开启热更新，监听: {config_path} 和 {theme_dir}")
    # 启动 HTTP 服务
    port = args.port
    
    # 切换到 dist 目录
    original_cwd = os.getcwd()
    os.chdir(dist_dir)
    
    # 创建服务器时启用端口重用
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"🌐 本地预览服务已启动: http://localhost:{port}")
        print("按 Ctrl+C 停止服务。")
        try:
            while True:
                httpd.handle_request()
        except KeyboardInterrupt:
            print("\n正在停止服务...")
        finally:
            # 确保正确关闭服务器和观察者
            httpd.server_close()
            observer.stop()
            observer.join()
            # 恢复原始工作目录
            os.chdir(original_cwd)
            print("服务已停止，端口已释放。")

def list_themes(args):
    """列出当前支持的主题"""
    themes = [
        ("enterprise", "企业官网"),
        ("saas", "SaaS 平台"), 
        ("ecommerce", "电商平台"),
        ("blog", "个人博客"),
        ("news", "新闻网站")
    ]
    
    print("Available themes:")
    print()
    
    for name, title in themes:
        print(f"  {name:<12} {title}")
    
    print()
    print("Examples:")
    print("  python ptfy.py build --theme enterprise")
    print("  python ptfy.py preview --theme saas")

def main():
    parser = argparse.ArgumentParser(description="PageTemplatify (ptfy) - 静态 HTML 页面生成器")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # build 子命令
    parser_build = subparsers.add_parser('build', help='生成静态页面')
    parser_build.add_argument('--theme', '-t', required=True, 
                             choices=['enterprise', 'saas', 'ecommerce', 'blog', 'news'],
                             help='主题名称')
    parser_build.add_argument('--config', '-c', help='自定义配置文件路径（可选）')
    parser_build.set_defaults(func=build)

    # preview 子命令
    parser_preview = subparsers.add_parser('preview', help='本地预览 dist 目录，支持热更新')
    parser_preview.add_argument('--theme', '-t', required=True,
                               choices=['enterprise', 'saas', 'ecommerce', 'blog', 'news'],
                               help='主题名称')
    parser_preview.add_argument('--config', '-c', help='自定义配置文件路径（可选）')
    parser_preview.add_argument('--port', '-p', type=int, default=9469, help='预览服务端口，默认 9469')
    parser_preview.set_defaults(func=preview)

    # list 子命令
    parser_list = subparsers.add_parser('list', help='列出当前支持的主题')
    parser_list.set_defaults(func=list_themes)

    args = parser.parse_args()
    
    # 只有 build 和 preview 命令需要 config 属性
    if hasattr(args, 'theme') and not hasattr(args, 'config'):
        args.config = None
    
    # 如果没有指定 config，使用与 theme 同名的配置文件
    if hasattr(args, 'config') and not args.config and hasattr(args, 'theme'):
        args.config = f"configs/{args.theme}.json"
    
    args.func(args)

if __name__ == '__main__':
    main()
