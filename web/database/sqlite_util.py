import sqlite3
import  os
import datetime
def createTable():
    """创建数据库表"""
    # 如果表不存在，则创建
    sql = """CREATE TABLE IF NOT EXISTS VOICE(
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                f_path TEXT NOT NULL,
                voice_len INT NOT NULL,
                possble_section TEXT NOT NULL,
                created_time TEXT,
                updated_time TEXT
                );"""
    # 执行SQL指令
    cursor.execute(sql)

def saveVoiceRecord(path,voice_len,possble_section):
    #查看
    created_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    updated_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    sql = 'insert into VOICE (id,f_path,voice_len,possble_section,created_time,updated_time) values(NULL,"%s",%d,"%s","%s","%s");'%(path,voice_len,possble_section,created_time,updated_time)
    print(sql)
    cursor.execute(sql)
    conn.commit()

    pass
def deleteVoiceRecord(id):
    sql = "delete from VOICE where id = %d"%id
    cursor.execute(sql)
    conn.commit()

    pass

#TODO  这里需要来个分页的，不然后面数据一多的话，不好找
def getallVoiceRecord():
    sql = """
        SELECT * from VOICE
    """
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
    return result

#设置当前数据库存在的绝对路径
cur_path = os.path.dirname(os.path.realpath(__file__))
print(cur_path)
conn = sqlite3.connect(database=os.path.join(cur_path,"vad.db"),check_same_thread=False)
cursor = conn.cursor()
createTable()
# saveVoiceRecord("222",11,"fuck")



