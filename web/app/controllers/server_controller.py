import csv
import traceback

from flask import request, Blueprint, current_app, jsonify

from web.app.models.ServerModel import ServerModel
from web.database.db import get_db
from web.untils.encrypt import cry_pass,decode_pass

# 定义控制器蓝图
sc = Blueprint('server', __name__, url_prefix='/server')
running_server_list = {}
reload_server = True

# 获取服务器列表
@sc.route('/')
def index():
    db = get_db()
    sql_result = db.execute(
        'SELECT * FROM servers'
    ).fetchall()
    result = []
    for i in sql_result:
        result.append({"id": i[0], "server_name": i[1]})
    return jsonify(result)

# 获取单个服务器
@sc.route('/show/<id>')
def show(id):
    db = get_db()
    i = db.execute(
        'SELECT * FROM servers WHERE id = '+id
    ).fetchone()
    return {
        "server_name":i[1],
        "server_ip":i[2],
        "server_port": i[3],
        "server_username": i[4],
        "server_pwd": decode_pass(i[5]),
        "mysql_ip": i[6],
        "mysql_port": i[7],
        "mysql_username": i[8],
        "mysql_password": decode_pass(i[9]),
        "sql_server_ip": i[10],
        "sql_server_port": i[11],
        "sql_server_username": i[12],
        "sql_server_password": decode_pass(i[13]),
        "oracle_ip": i[14],
        "oracle_port": i[15],
        "oracle_username": i[16],
        "oracle_password": decode_pass(i[17]),
        "oracle_db": i[18],
        "oracle_type": i[19],
    }

# 删除服务器
@sc.route('/destroy/<id>')
def destroy(id):
    global reload_server
    # # 停止监控，删除列表
    # if(int(id) in running_server_list):
    #     running_server_list[int(id)].stop()
    #     del(running_server_list[int(id)])
    # 删除记录
    db = get_db()
    db.execute(
        'DELETE FROM servers WHERE id = ?',(id)
    )
    db.commit()
    # 刷新监控列表
    reload_server = True
    return {
        "code":1,
        "msg":"success"
    }

@sc.route('/create',methods=["POST"])
def create():
    global reload_server
    # 获取参数，并验证
    data = {
        "server_name": request.json.get("server_name",""),
        "server_ip": request.json.get("server_ip",""),
        "server_port": request.json.get("server_port",0),
        "server_username": request.json.get("server_username",""),
        "server_pwd": cry_pass(request.json.get("server_pwd","")),
        "mysql_ip": request.json.get("mysql_ip",""),
        "mysql_port": request.json.get("mysql_port",0),
        "mysql_username": request.json.get("mysql_username",""),
        "mysql_password": cry_pass(request.json.get("mysql_password","")),
        "sql_server_ip": request.json.get("sql_server_ip",""),
        "sql_server_port": request.json.get("sql_server_port",0),
        "sql_server_username": request.json.get("sql_server_username",""),
        "sql_server_password": cry_pass(request.json.get("sql_server_password","")),
        "oracle_ip": request.json.get("oracle_ip",""),
        "oracle_port": request.json.get("oracle_port",0),
        "oracle_username": request.json.get("oracle_username",""),
        "oracle_password": cry_pass(request.json.get("oracle_password","")),
        "oracle_db": request.json.get("oracle_db",""),
        "oracle_type": request.json.get("oracle_type",0),
    }
    # 加入数据库
    try:
        db = get_db()
        db.execute(
            """INSERT INTO servers("s_name", "s_ip", "s_port", "s_username", "s_pwd", "m_ip", "m_port", "m_username", "m_pwd", "ms_ip", "ms_port", "ms_username", "ms_pwd", "o_ip", "o_port", "o_username", "o_pwd", "o_db", "o_type") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """,
            (
                data["server_name"], data["server_ip"], data["server_port"], data["server_username"],
                data["server_pwd"], data["mysql_ip"], data["mysql_port"], data["mysql_username"],
                data["mysql_password"], data["sql_server_ip"], data["sql_server_port"], data["sql_server_username"],
                data["sql_server_password"], data["oracle_ip"], data["oracle_port"], data["oracle_username"],
                data["oracle_password"], data["oracle_db"], data["oracle_type"],
            )
        )
        db.commit()
    except:
        traceback.print_exc()
        return {
        "code":-1,
        "msg":"fail to add"
    }
    # 刷新监控列表
    reload_server = True

    return {
        "code":1,
        "msg":"success"
    }

@sc.route('/update',methods=["POST"])
def update():
    global reload_server
    # 获取参数，并验证
    data = {
        "id": request.json.get("id", ""),
        "server_name": request.json.get("server_name", ""),
        "server_ip": request.json.get("server_ip", ""),
        "server_port": request.json.get("server_port", 0),
        "server_username": request.json.get("server_username", ""),
        "server_pwd": cry_pass(request.json.get("server_pwd", "")),
        "mysql_ip": request.json.get("mysql_ip", ""),
        "mysql_port": request.json.get("mysql_port", 0),
        "mysql_username": request.json.get("mysql_username", ""),
        "mysql_password": cry_pass(request.json.get("mysql_password", "")),
        "sql_server_ip": request.json.get("sql_server_ip", ""),
        "sql_server_port": request.json.get("sql_server_port", 0),
        "sql_server_username": request.json.get("sql_server_username", ""),
        "sql_server_password": cry_pass(request.json.get("sql_server_password", "")),
        "oracle_ip": request.json.get("oracle_ip", ""),
        "oracle_port": request.json.get("oracle_port", 0),
        "oracle_username": request.json.get("oracle_username", ""),
        "oracle_password": cry_pass(request.json.get("oracle_password", "")),
        "oracle_db": request.json.get("oracle_db", ""),
        "oracle_type": request.json.get("oracle_type", 0),
    }
    # 加入数据库
    try:
        db = get_db()
        db.execute(
            """UPDATE servers SET "s_name"=?, "s_ip"=?, "s_port"=?, "s_username"=?, "s_pwd"=?, "m_ip"=?, "m_port"=?, "m_username"=?, "m_pwd"=?, "ms_ip"=?, "ms_port"=?, "ms_username"=?, "ms_pwd"=?, "o_ip"=?, "o_port"=?, "o_username"=?, "o_pwd"=?, "o_db"=?, "o_type"=? WHERE "id"=? """,
            (
                data["server_name"], data["server_ip"], data["server_port"], data["server_username"],
                data["server_pwd"], data["mysql_ip"], data["mysql_port"], data["mysql_username"],
                data["mysql_password"], data["sql_server_ip"], data["sql_server_port"], data["sql_server_username"],
                data["sql_server_password"], data["oracle_ip"], data["oracle_port"], data["oracle_username"],
                data["oracle_password"], data["oracle_db"], data["oracle_type"],data["id"]
            )
        )
        db.commit()
    except:
        traceback.print_exc()
        return {
            "code": -1,
            "msg": "fail to add"
        }

    # 刷新监控列表
    reload_server = True

    return {
        "code": 1,
        "msg": "success"
    }

@sc.route('/data/<id>')
def data(id):
    load_all_server()

    # 判断id在不在列表中
    if(int(id) not in running_server_list):
        return {"code":-1,"msg":"cannot find server"}

    # 获取数据
    return {"code": 1, "msg": "success", "data": running_server_list[int(id)].table_data}

def load_all_server():
    global  reload_server
    # 判断服务器加载了吗
    if(reload_server):
        # 停止所有服务器
        for i in running_server_list:
            running_server_list[i].stop()
        running_server_list.clear()
        # 加载所有服务器
        sql_result = get_db().execute(
            'SELECT * FROM servers'
        ).fetchall()
        # 加入监控数组
        for i in sql_result:

            # 新建服务器
            sm = ServerModel()
            sm.server_name = i[1]

            sm.server_ip = i[2]
            sm.server_port = i[3]
            sm.server_username = i[4]
            sm.server_pwd = decode_pass(i[5])

            sm.mysql_ip = i[6]
            sm.mysql_port = i[7]
            sm.mysql_username = i[8]
            sm.mysql_password = decode_pass(i[9])

            sm.sql_server_ip = i[10]
            sm.sql_server_port = i[11]
            sm.sql_server_username = i[12]
            sm.sql_server_password = decode_pass(i[13])

            sm.oracle_ip = i[14]
            sm.oracle_port = i[15]
            sm.oracle_username = i[16]
            sm.oracle_password = decode_pass(i[17])
            sm.oracle_db = i[18]
            sm.oracle_type = i[19]

            # 运行，并加入服务器
            sm.connect()
            sm.start()
            sm.init_app()
            # 加入运行服务器
            running_server_list[i[0]]=sm

        reload_server = False
    else:
        # 判断有没有没加载的警报数据
        for i in running_server_list:
            for j in running_server_list[i].db_data:
                try:
                    db = get_db()
                    db.execute(
                        """INSERT INTO alerts("content", "alert_server", "created_at") VALUES (?,?,?) """,
                        j
                    )
                    db.commit()
                except:
                    print("插入数据库失败")
                    traceback.print_exc()
            running_server_list[i].db_data = []
    # 若已经加载，则判断有没有要重连的
    # for i in running_server_list:
    #     if(running_server_list[i].ssh == None):
    #         running_server_list[i].connect()