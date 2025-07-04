#!/usr/bin/env python3
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

def main():
    parser = argparse.ArgumentParser(description="PageTemplatify (ptfy) - 静态 HTML 页面生成器")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # build 子命令
    parser_build = subparsers.add_parser('build', help='生成静态页面')
    parser_build.add_argument('--config', '-c', required=True, help='JSON 配置文件路径')
    parser_build.add_argument('--theme', '-t', default='default', help='主题名称，默认 default')
    parser_build.set_defaults(func=build)

    # preview 子命令
    parser_preview = subparsers.add_parser('preview', help='本地预览 dist 目录，支持热更新')
    parser_preview.add_argument('--config', '-c', required=True, help='JSON 配置文件路径')
    parser_preview.add_argument('--theme', '-t', default='default', help='主题名称，默认 default')
    parser_preview.add_argument('--port', '-p', type=int, default=9469, help='预览服务端口，默认 9469')
    parser_preview.set_defaults(func=preview)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
