#!/usr/bin/env python3
"""
台灣大逃亡：颱風來啦！(Typhoon Escape Taiwan) - 本地預覽伺服器
"""
import http.server
import socketserver
import os
import sys
import webbrowser

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def start_server():
    port = PORT
    while port < PORT + 20:
        try:
            with socketserver.TCPServer(("", port), Handler) as httpd:
                url_tw = f"http://localhost:{port}/index.html"
                url_orig = f"http://localhost:{port}/references/original-typhoon-escape/index.html"
                print("=" * 66)
                print(" 🇹🇼 台灣大逃亡：颱風來啦！(Typhoon Escape Taiwan) - 開發伺服器")
                print("=" * 66)
                print(f" 🎮 台灣在地化旗艦版:  {url_tw}")
                print(f" 🇯🇵 日本原版離線對照:  {url_orig}")
                print(f" 📂 專案根目錄路徑:    {DIRECTORY}")
                print(" 按下 Ctrl+C 即可關閉伺服器")
                print("=" * 66)
                
                # 自動開啟預設瀏覽器至台灣版
                try:
                    webbrowser.open(url_tw)
                except Exception:
                    pass
                    
                httpd.serve_forever()
                break
        except OSError:
            port += 1

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n伺服器已關閉。感謝遊玩！")
