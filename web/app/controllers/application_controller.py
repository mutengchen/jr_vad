import csv
import glob
import json
import os
import sqlite3
from web.database.sqlite_util import createTable
from flask import redirect, Blueprint, request, render_template, send_file,url_for
from ast import literal_eval
from vad.VadModel import VadModel
from web.database.sqlite_util import getallVoiceRecord
appc = Blueprint('application', __name__, url_prefix='/')

model = VadModel()


@appc.route('/')
def index():
    #查找当前数据库里面的所有语音记录
    data_list = getallVoiceRecord()
    print(data_list)
    temp = []
    for item in data_list:
        #这里的section需要转换下，让前段不需要计算
        section_list = literal_eval(item[3])
        result = []
        last_end = 0
        for s_item in section_list:
            #每一个百分比乘以当前进度条的长度，当前进度条长度为200px
            if last_end==0:
                result.append([s_item[0]*200,s_item[1]*200,0])
            else:
                result.append([s_item[0]*200,s_item[1]*200,s_item[0]*200-last_end])
            last_end = s_item[1]*200
        print(result)
        temp.append({"id":item[0],"path":item[1],"voice_len":item[2],"section":result,"created_time":item[4]})
    kwargs = {"data": temp}
    return render_template("mainpage.html",**kwargs)



@appc.route('/voice_list')
def voice_list():
    data_list = getallVoiceRecord()
    print(data_list)
    temp = []
    for item in data_list:
        # 这里的section需要转换下，让前段不需要计算
        section_list = literal_eval(item[3])
        result = []
        last_end = 0
        for s_item in section_list:
            print(s_item)
            # 每一个百分比乘以当前进度条的长度，当前进度条长度为200px
            if last_end == 0:
                result.append({"width":"%.3fpx"%(s_item[1]* 200-s_item[0] * 200),"left":"0px"} )
            else:
                result.append({"width":"%.3fpx"%(s_item[1] * 200-s_item[0] * 200),"left": "%.3fpx"%(int(s_item[0] * 200 - last_end))})
            last_end = s_item[1] * 200
        print(result)
        temp.append({"id": item[0], "path": item[1], "voice_len": item[2], "section": result, "created_time": item[4]})
        return json.dumps(temp)

@appc.route('/upload')
def upload():
    return render_template("upload.html")
@appc.route('/uploader', methods=['GET', 'POST'])
def uploader():
    """
        文件上传
    """
    if request.method == 'POST':
        # input标签中的name的属性值
        f = request.files['file']
        # 拼接地址，上传地址，f.filename：直接获取文件名
        f.save(os.path.join(model.upload_folder, f.filename))
        # 输出上传的文件名
        print(request.files, f.filename)
        # 读取保存完成音频文件开始转换文件，然后返回文件
        model.start(f.filename)
        #重定向回首页
        return {"code":200,"result":"上传完成"}



@appc.route('/download/<filename>')
def download_file(filename):
    # 构造供下载文件的完整路径
    path = os.path.join(model.cur_path, "output/%s"%filename)
    return send_file(path, as_attachment=True)
