import csv
from flask import request,Blueprint

# 定义控制器蓝图
from web.database.db import get_db

ac = Blueprint('alert', __name__, url_prefix='/alert')

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
@ac.route('/')
def alert():
   # 获取警报页面参数
   if "current_page" not in request.args or "count_per_page" not in request.args:
      current_page = 1
      count_per_page = 10
   else:
      current_page = int(request.args["current_page"])
      count_per_page = int(request.args["count_per_page"])

   # 判断参数
   if(current_page <= 0):
      return {"code":"-1","msg":"current_page error"}
   if (count_per_page <= 0):
      return {"code": "-1", "msg": "count_per_page error"}

   # # 读取文件
   # result = []
   # count = 0
   # with open("data/alert.data") as f:
   #    for index,row in enumerate(csv.reader(f)):
   #       count +=1
   #       if(index>=(current_page-1)*count_per_page and index<(current_page-1)*count_per_page+count_per_page):
   #          result.append({"id":int(row[0]),"content":row[1],"alert_type":row[2],"created_at":row[3],"alert_server":row[4],"alert_opera":row[5]})

   db = get_db()
   sql_result = db.execute(
      'SELECT id,content,alert_server,created_at FROM alerts'
   ).fetchall()
   result = []
   for i in sql_result:
      result.append({"id": i[0], "content": i[1],"alert_server": i[2],"created_at": i[3]})

   sql_result = db.execute(
      'SELECT COUNT(1) FROM alerts'
   ).fetchone()
   return {"code":1,"message":"success","count":sql_result[0],"data":result}

# @ac.route('/')
# def index():
#     db = get_db()
#     posts = db.execute(
#         'SELECT * FROM alerts'
#     )
#     print(posts)
#     return posts