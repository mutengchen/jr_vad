import traceback

import pymysql,pymssql,cx_Oracle
# from sshtunnel import SSHTunnelForwarder

# MYSQL 查看表空间的语句
COMMAND_MYSQL_TABLE_SPACE = """
select
    table_schema,
    sum(truncate(data_length/1024/1024, 2))+sum(truncate(index_length/1024/1024, 2))
from information_schema.tables
group by table_schema
order by sum(data_length) desc, sum(index_length) desc;
"""
# SQL SERVER 查看表空间的语句
COMMAND_MSSQL_TABLE_SPACE = """
SELECT t.DatabaseName, SUM(t.SizeMB) FROM
(SELECT DB_NAME(database_id) AS DatabaseName, (size*8.0)/1024 SizeMB FROM sys.master_files) AS t
GROUP BY t.DatabaseName
"""
# ORACLE查看表空间的语句
COMMAND_ORACLE_TABLE_SPACE = """
select tablespace_name, sum(bytes)/1024/1024 from dba_data_files group by tablespace_name
"""
def create_ssh_channel(host, port, username):
    pass

# 使用ssh通道执行代码
# def use_ssh_tunnel(host, port, username, password, remote_port, local_port, func):
#     with SSHTunnelForwarder(
#         ssh_address_or_host=(host, port),
#         ssh_username=username,
#         ssh_password=password,
#         remote_bind_address=(host, remote_port),
#         local_bind_address=('127.0.0.1', local_port)
#     ) as server:
#         server.start()
#         # 执行功能
#         func()
#         server.close()

# 获取mysql表空间
# https://blog.51cto.com/u_15072778/4531278
def get_mysql_table_space(host, port, username, password, database="", charset="utf8"):
    try:
        db_sqls = pymysql.connect(host=host, port=port, user=username, password=password, database=database,
                                  charset=charset, connect_timeout=10)  # 连接SQLServer
        # host后面接数据库服务器所在的ip地址，port是端口号，一般为默认值，user是访问者的用户名，password是访问者的密码，database是需要访问的某个数据库名称，charset是？？？等下查一下
        cur_sqls = db_sqls.cursor()  # SQLServer的游标

        # 执行语句较多，单独写出来
        sql = COMMAND_MYSQL_TABLE_SPACE  # 一定要用三对双引号，并且数据库语句最后不要有分号";"
        success_count = cur_sqls.execute(sql)  # 执行数据库相应的语句
        mysql_res = cur_sqls.fetchall()
        mysql_table_name = []
        mysql_table_size = []
        # 加入结果
        for i in mysql_res:
            mysql_table_name.append(i[0])
            mysql_table_size.append(float(i[1]))

        cur_sqls.close()  # 关闭游标
        db_sqls.commit()  # 提交，有些数据库引擎无需此行
        db_sqls.close()  # 关闭数据库连接
    except:
        traceback.print_exc()
        return [],[]
    return mysql_table_name, mysql_table_size


# 获取mssql表空间
# https://blog.51cto.com/u_15072778/4531278
def get_mssql_table_space(host, port, username, password, database="", charset="utf8"):
    db_sqls = pymssql.connect(host=host, port=port, user=username, password=password, database=database,
                              charset=charset)  # 连接SQLServer
    # host后面接数据库服务器所在的ip地址，port是端口号，一般为默认值，user是访问者的用户名，password是访问者的密码，database是需要访问的某个数据库名称，charset是？？？等下查一下
    cur_sqls = db_sqls.cursor()  # SQLServer的游标

    # 执行语句较多，单独写出来
    sql = COMMAND_MSSQL_TABLE_SPACE  # 一定要用三对双引号，并且数据库语句最后不要有分号";"
    success_count = cur_sqls.execute(sql)  # 执行数据库相应的语句
    mssql_res = cur_sqls.fetchall()
    mssql_table_name = []
    mssql_table_size = []
    # 加入结果
    for i in mssql_res:
        mssql_table_name.append(i[0])
        mssql_table_size.append(float(i[1]))
    cur_sqls.close()  # 关闭游标
    db_sqls.commit()  # 提交，有些数据库引擎无需此行
    db_sqls.close()  # 关闭数据库连接
    return mssql_table_name, mssql_table_size

# 获取oracle表空间
# TODO windows下测试
def get_oracle_table_space(host, port, username, password, database):
    # 建立连接
    db = cx_Oracle.connect(username, password, host+":"+str(port)+"/"+database)
    # 获取游标
    cursor = db.cursor()
    # 查询数据
    cursor.execute(COMMAND_ORACLE_TABLE_SPACE)
    # 获取数据
    data = cursor.fetchall()
    table_name = []
    table_size = []
    # 加入结果
    for i in data:
        table_name.append(i[0])
        table_size.append(float(i[1])/1024)
    db.commit()
    cursor.close()
    db.close()
    return table_name, table_size