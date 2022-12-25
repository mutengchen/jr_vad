# 关闭窗口
class API():
    def set_webview(self, webview):
        self.webview = webview

    def close_webview(self):
        self.webview.destroy()

    def mini_webview(self):
        self.webview.minimize()
