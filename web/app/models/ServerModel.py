import random
import time
import threading
import paramiko
import traceback
import webview
from flask import current_app
from web.untils.command_linux import get_cpu, get_date,get_mem,get_disk
from web.untils.command_database import get_oracle_table_space,get_mysql_table_space,get_mssql_table_space
from web.untils.encrypt import cry_pass,decode_pass
from web.untils import wechat_untils,sms_untils,mail_untils
from web.app.models.AlertModel import AlertModel
from web.database.db import get_db


# TODO 怎么快速生成模型？
# 服务类
class ServerModel():
    def __init__(self):
        # 服务器配置
        self.server_name = ""               # 服务器名
        self.server_ip = ""                 # 服务器IP
        self.server_username = ""           # 用户名
        self.server_pwd = ""                # 服务器密码
        self.server_port = 22

        # 数据库配置
        self.mysql_ip = ""
        self.mysql_username = ""
        self.mysql_password = ""
        self.mysql_port = 3306
        self.sql_server_ip = ""
        self.sql_server_username = ""
        self.sql_server_password = ""
        self.sql_server_port = 1433
        self.oracle_ip = ""
        self.oracle_username = ""
        self.oracle_password = ""
        self.oracle_port = 1521
        self.oracle_db = ""
        self.oracle_type = 0

        self.mysql_connect = True
        self.sql_server_connect = True
        self.oracle_connect = True

        # 配置项
        self.cpu_threshold = 0.95
        self.memory_threshold = 0.95
        self.disk_threshold = 0.95
        self.table_size_threshold = 4 * 1024 * 1024
        self.alert_opera = 0                 # 操作类型  位运算 从左到右  弹窗，邮件，微信
        # 服务器状态
        # 0 未开始监控
        # 1 正常监控中
        # 2 3 4无需监控mysql sql_server, oracle
        # -1 服务器未启动
        # -2 -3 -4无法监控mysql sql_server, oracle
        self.server_status = 0
        self.start_monitor=False
        # 上次报警时间，0-5分别是CPU，内存，硬盘，mysql,mssql,oracle连接不上的信息时间戳，6-11是报警的时间戳
        self.alert_time = [0 for i in range(12)]
        # 服務器顯示的表格數據
        self.table_data = [{"title":"CPU使用率","x":[],"y":[]},
                           {"title":"内存使用率","x":[],"y":[]},
                           {"title":"硬盘使用情况","x":[],"y":[]},
                           {"title":"Mysql","x":[],"y":[]},
                           {"title":"SQL Server","x":[],"y":[]},
                           {"title":"Oracle","x":[],"y":[]}]
        # 缓冲区
        self.db_data = []
        # 限制
        self.cpu_mem_threshold = 100

    # 初始化web信息
    def init_app(self):
        # 限制比率
        self.disk_threshold = current_app.config.get("DISK_THRESHOLD")
        self.mysql_threshold = current_app.config.get("MYSQL_THRESHOLD")
        self.mssql_threshold = current_app.config.get("MSSQL_THRESHOLD")
        self.oracle_threshold = current_app.config.get("ORACLE_THRESHOLD")
        self.cpu_mem_threshold = current_app.config.get("CPU_MEM_THRESHOLD")
        self.alert_interval = current_app.config.get("ALERT_INTERVAL")
        self.use_wechat = True if current_app.config.get("USE_WECHAT")==1 else False
        self.use_sms = True if current_app.config.get("USE_SMS")==1 else False
        self.use_mail = True if current_app.config.get("USE_MAIL")==1 else False
        self.phone = current_app.config.get("SMS_PHONE")
        self.wechat_name = current_app.config.get("WECHAT_NAME")
        self.mail_sender = current_app.config.get("MAIL_SENDER")
        self.mail_password = current_app.config.get("MAIL_PASSWORD")
        self.mail_notify = current_app.config.get("MAIL_NOTIFY")
        self.db = get_db()

    # 连接，若失败就重新连接
    def connect(self):
        if(not self.server_ip or not self.server_port or not self.server_username or not self.server_pwd or len(self.server_ip)<=0 or len(self.server_pwd) <=0 or self.server_port<=0 or len(self.server_username)<=0):
            self.ssh = None
        else:
            try:
                # 创建ssh
                self.ssh = paramiko.SSHClient()
                # 设置信任远程机器，允许访问
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            except:
                self.ssh = None
                print("There is an error with the SSHClient")
                traceback.print_exc()

            try:
                # 设置ssh远程连接机器，参数依次为地址、端口、用户名、密码,ssh端口默认22
                self.ssh.connect(self.server_ip,
                            self.server_port,
                            self.server_username,
                            self.server_pwd)
            except:
                self.ssh = None
                print("Failed to connect to remote server")
                traceback.print_exc()

        # print(self.server_name,self.mysql_ip,self.mysql_port,self.mysql_username,self.mysql_password)
        if (not self.mysql_ip or not self.mysql_port or not self.mysql_username or not self.mysql_password or len(
            self.mysql_ip) <= 0 or len(self.mysql_password) <= 0 or self.mysql_port <= 0 or len(
            self.mysql_username) <= 0):
            self.mysql_connect = False
        if (not self.sql_server_ip or not self.sql_server_port or not self.sql_server_username or not self.sql_server_password or len(
            self.sql_server_ip) <= 0 or len(self.sql_server_password) <= 0 or self.sql_server_port <= 0 or len(
            self.sql_server_username) <= 0):
            self.sql_server_connect = False
        if (not self.oracle_db or not self.oracle_type or not self.oracle_ip or not self.oracle_port or not self.oracle_username or not self.oracle_password or len(
            self.oracle_ip) <= 0 or len(self.oracle_password) <= 0 or self.oracle_port <= 0 or len(
            self.oracle_username) <= 0 or len(self.oracle_db)<=0 or self.oracle_type<=0):
                self.oracle_connect = False

    # 更新cpu和内存
    def update_cpu_and_mem(self):
        try:
            # 获取设备信息
            curr_time = get_date(self.ssh)
            if(curr_time == None):
                # 报警
                return -1,"无法连接服务器"
            cpu_usage = get_cpu(self.ssh)
            mem_usage = get_mem(self.ssh)
            # 添加到表格中
            if(len(self.table_data[0]["x"])==60):
                del(self.table_data[0]["x"][0])
                del(self.table_data[0]["y"][0])
            self.table_data[0]["x"].append(curr_time)
            self.table_data[0]["y"].append(cpu_usage)
            if (len(self.table_data[1]["x"]) == 60):
                del (self.table_data[1]["x"][0])
                del (self.table_data[1]["y"][0])
            self.table_data[1]["x"].append(curr_time)
            self.table_data[1]["y"].append(mem_usage)

            # 判断使用率
            if(float(cpu_usage)>=self.cpu_mem_threshold):
                return -1,"CPU占用率过高"
            if (float(mem_usage) >= self.cpu_mem_threshold):
                return -1, "内存占用率过高"
            return 1,""
        except:
            print('Fail to update_cpu_and_mem')
            traceback.print_exc()
            return -1,"连接服务器异常"

    # 更新表空间
    def update_disk_and_space(self):
        try:
            # 获取硬盘
            disk_x, disk_y = get_disk(self.ssh)
            # 硬盘添加到表格中
            self.table_data[2]["x"]=disk_x
            self.table_data[2]["y"]=disk_y
            # 判断
            if(self.ssh != None):
                for i in disk_y:
                    if (float(i) >= self.disk_threshold):
                        self.call_alert(2, "服务器警报", "磁盘占用率过高")
            # 获取表空间
            # Mysql
            mysql_x, mysql_y = [], []
            if (self.mysql_connect):
                # 异步处理
                threading.Thread(target=self.update_mysql).start()
            # SQL Server
            ms_x, ms_y = [], []
            if(self.sql_server_connect):
                # 异步处理
                threading.Thread(target=self.update_mssql).start()
            # Oracle
            o_x, o_y = [], []
            if(self.oracle_connect):
                # 异步处理
                threading.Thread(target=self.update_oracle).start()

            return 1, {"data":[disk_x,disk_y,mysql_x,mysql_y,ms_x,ms_y,o_x,o_y]}
        except:
            print('Fail to update_disk_and_space')
            traceback.print_exc()

    # 数据库处理全部做异步操作
    def update_mysql(self):
        mysql_x, mysql_y = get_mysql_table_space(self.mysql_ip, self.mysql_port, self.mysql_username,
                                                 self.mysql_password)
        self.table_data[3]["x"] = mysql_x
        self.table_data[3]["y"] = mysql_y
        # 判断是否需要报警
        for i in mysql_y:
            if (float(i) >= self.mysql_threshold):
                self.call_alert(3, "服务器警报", "Mysql占用率过高")
                break
    def update_mssql(self):
        ms_x, ms_y = get_mssql_table_space(self.sql_server_ip, self.sql_server_port, self.sql_server_username,
                                           self.sql_server_password)

        self.table_data[4]["x"] = ms_x
        self.table_data[4]["y"] = ms_y
        for i in ms_y:
            if (float(i) >= self.mssql_threshold):
                self.call_alert(4,"服务器警报", "SQL Server占用率过高")
                break

    def update_oracle(self):
        o_x, o_y = get_oracle_table_space(self.oracle_ip, self.oracle_port, self.oracle_username, self.oracle_password,
                                          self.oracle_db)
        self.table_data[5]["x"] = o_x
        self.table_data[5]["y"] = o_y
        for i in o_y:
            if (float(i) >= self.oracle_threshold):
                self.call_alert(5,"服务器警报", "Oracle占用率过高")
                break

    def start(self):
        # 先停止原有线程
        self.stop()
        self.start_monitor = True
        threading.Thread(target=self.run).start()

    def stop(self):
        if(self.start_monitor):
            self.start_monitor = False
            time.sleep(1)
        else:
            self.start_monitor = False

    # 开始获取数据
    def run(self):
        if(self.ssh==None and self.mysql_connect and self.sql_server_connect and self.oracle_connect):
            return
        # 计时
        count = 0
        while(self.start_monitor):
            # 每隔1s更新 cpu和内存
            code, data = self.update_cpu_and_mem()
            if(code == -1):
                # 推送警报
                self.call_alert(1, "服务器警报", data)
            # 每隔15s 更新硬盘，表空间
            if (count == 0):
                self.update_disk_and_space()
            # 重置计时器
            if (count == 14):
                count = 0
            count += 1
            time.sleep(1)
        self.start_monitor = False

    # 推送警报
    def call_alert(self, error_type, title, content):
        try:
            # 修改错误的时间戳
            now = int(time.time())
            # 判断是否到报警时间了
            if(now - self.alert_time[error_type] >= self.alert_interval):
                # 记录时间
                self.alert_time[error_type] = now
                # 警报内容
                current = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                server = self.server_name + "(" + self.server_ip + ")"
                content = content + " ：" + self.server_name + "(" + self.server_ip + ")"
                # 弹框
                webview.create_window("预警 - "+current, html='<div style="display: flex;flex-direction: column;align-items: center">'+content+'<div>',width=400,height=95)
                # 推送警报
                try:
                    if self.use_wechat:
                        wechat_untils.callWechat(self.wechat_name)
                except:
                    print("微信调用失败"+traceback.format_exc())
                try:
                    if self.use_sms and self.phone != None:
                        sms_untils.send_sms(self.phone, self.server_ip, content)
                except:
                    print("短信调用失败"+traceback.format_exc())
                try:
                    if self.use_mail:
                        mail_untils.send_mail(self.mail_sender,self.mail_password,self.mail_notify,title, content)
                except:
                    print("邮件发送失败"+traceback.format_exc())
                self.db_data.append([content, server, current])

        except:
            traceback.print_exc()
            print("发送信息异常")