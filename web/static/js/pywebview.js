function initWindows(mini_btn, close_btn){
    // 隐藏滚动条
    $("body").css("overflow","hidden")
    // 画面允许滚动
    $("body").addClass('pywebview-drag-region')
    // 添加单击事件
    mini_btn.click(function () {
        pywebview.api.mini_webview()
    })
    close_btn.click(function () {
        pywebview.api.close_webview()
    })
}