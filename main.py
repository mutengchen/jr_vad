"""
main.py
"""
import os
import sys
import webview
from apis import API
from web import create_app

# 将web包加入代码环境变量
sys.path.append(os.path.join("..","web"))

# 创建api
api = API()
# 创建窗口
window = webview.create_window(
    title='资源预警小哨兵',
    url=create_app(),
    js_api=api,
    width=1040,
    height=677,
    resizable=False,  # 固定窗口大小
    text_select=False,  # 禁止选择文字内容
    confirm_close=False,  # 关闭时提示
    frameless=True  # 无边框
)
# 设置API
api.set_webview(window)

webview.start(debug=True, http_server=True)

