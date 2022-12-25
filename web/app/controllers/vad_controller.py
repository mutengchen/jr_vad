from flask import request, Blueprint, redirect

# 定义控制器蓝图
from web.database.db import get_db

vad = Blueprint('vad', __name__, url_prefix='/vad')

# 接口文档
# 1. 获取警报接口
# - GET /alert/index
# - 参数
#   current_page 当前页码 ex. 6
#   count_per_page 每页数量 ex. 10
# - 成功的返回
#    {"code":1, "message":"success", "count":111, "data":[]} # count 警报总数， data 数据列表。里面包含如下字段
#    content = ""  # 报警信息
#    alert_type = 0  # 警告类型  0 服务器无法连接 1 cpu 2 memory 3 disk 4 mysql 5 sql_server 6 oracle
#    created_at = ""  # 发生时间
#    alert_server = ""  # 警告的服务器名(ip)
#    alert_opera = 0  # 操作类型  位运算 从左到右 邮件，微信，短信
# - 失败的返回
#  {"code":-1, "message":"失败原因"}
#   code 为负数时，表示发生错误，信息在message里面
@vad.route('/')
def upload():
    return redirect("/static/upload.html")