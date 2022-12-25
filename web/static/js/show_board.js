$(document).ready(function () {
    //刷新页面默认显示监控看板即面板1
    show_board(1)

    //刷新加载第一页数据
    show_alert_page(1)

    //鼠标点击事件 显示对应面板
    $("#control").click(function () {
        show_board(1)
    })
    $("#server").click(function () {
        show_board(2)
    })
    $("#warn").click(function () {
        show_board(3)
    })
    $("#system").click(function () {
        show_board(4)
    })
    // 点击右上角信息按钮跳转到警报管理界面
    $(".message").click(function () {
        show_board(3)
    })

})

//控制面板显示隐藏
function show_board(x) {
    $(".board").hide()
    $(".board:eq(" + (x - 1) + ")").show()

    $(".bot_left > ul > li").removeClass("list_hover")
    $(".bot_left > ul > li:nth-child(" + x + ")").addClass("list_hover")
    if (x == 3) {
        show_alert_page()
    }
}

//初始化分页器
function initPagination(r, page) {
    $(".zxf_pagediv").createPage({
        pageNum: Math.ceil(r.count / 10),
        current: page,
        backfun: function (e) {
            // 去服务器拿数据
            show_alert_page(e.current)
        }
    })
}

//是否已初始化分页器
let hasInitPagination = false;

// 获取页面数据
function show_alert_page(page) {
    // 装载在页面上
    $.ajax({
        type: "GET",
        url: "/alert/",
        data: { "current_page": page, "count_per_page": 99999 },
        success: function (r) {
            console.warn('警报信息列表', r)
            // console.warn('警报信息列表', alertTypeOpion(0))
            if (r.code = 1) {
                $(".tablebody").empty()
                // if (!hasInitPagination) {
                //     hasInitPagination = true;
                //     initPagination(r, page);
                // }
                setPageData(r)
            } else {
                alert("调用失败")
            }
        }
    })
}

//处理返回数据
function setPageData(r) {
    r.data = r.data.reverse()
    for (var index in r.data) {
        $(".tablebody").append("<tr>\n" +
            // "                        <td class=\"list1\">\n" +
            // "                            <input type=\"checkbox\">\n" +
            // "                        </td>\n" +
            "                        <td class=\"warn_project\">" + r.data[index].id + "</td>\n" +
            "                        <td class=\"warn_time\">" + r.data[index].created_at + "</td>\n" +
            "                        <td class=\"warn_content\">" + r.data[index].content + "</td>\n" +
            "                        <td class=\"warn_server\">" + r.data[index].alert_server + "</td>\n" +
            "                    </tr>")
    }
}

//判断项目类型
function alertTypeOpion(r) {
    if (r == 0) {
        return "服务器无法连接"
    }
    if (r == 1) {
        return "CPU"
    }
    if (r == 2) {
        return "memory"
    }
    if (r == 3) {
        return "disk"
    }
    if (r == 4) {
        return "mysql"
    }
    if (r == 5) {
        return "sql_server"
    }
    if (r == 6) {
        return "oracle"
    } else {
        return "无效"
    }
}

//判断警报通知方式
function alertOperaOpion(r) {
    if (r == 0) {
        return "弹窗"
    }
    if (r == 1) {
        return "邮件"
    }
    if (r == 2) {
        return "微信"
    }
    if (r == 3) {
        return "短信"
    } else {
        return "无通知"
    }
}