import time
import traceback
# 警报类
class AlertModel():
    def __init__(self):
        # 警报信息
        self.content = ""               # 服务器名
        self.alert_type = 0             # 警告类型  0 服务器无法连接 1 cpu 2 memory 3 disk 4 mysql 5 sql_server 6 oracle
        self.created_at = ""            # 发生时间
        self.alert_server = ""          # 警告的服务器名(ip)
        self.alert_opera = 0            # 操作类型  位运算 从左到右  弹窗，邮件，微信，短信

    @staticmethod
    def insert(db, content, alert_server, created_at):
        print(db)
        import time
        time.sleep(2)
        try:
            db.execute(
                """INSERT INTO alerts("content", "alert_server", "created_at") VALUES (?,?,?) """,
                (
                    content, alert_server, created_at
                )
            )
            db.commit()
        except:
            print("插入数据库失败")
            traceback.print_exc()
