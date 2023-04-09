import os
import os
import time
from pprint import pprint

import numpy as np
import torch
from IPython.display import Audio
from pydub import AudioSegment
from web.database.sqlite_util import saveVoiceRecord
from flask import send_file
import soundfile as sf
# from main import SAMPLING_RATE
import noisereduce as nr
# from noisereduce.utils import get_noise
# @app.route('/upload', methods=['GET', 'POST'])
# def upload_file():
#     # 渲染文件
#     return render_template('upload.html')
from pydub.silence import split_on_silence
# 文件保存的目录，根据实际情况的文件结构做调整；
# 若不指定目录，可以写成f.save(f.filename)，可以默认保存到当前文件夹下的根目录
# 设置上传文件保存路径 可以是指定绝对路径，也可以是相对路径（测试过）
# 将地址赋值给变量
from .utils_vad import init_jit_model,get_speech_timestamps,save_audio,read_audio,collect_chunks
class VadModel():

    def __init__(self):
        self.cur_path = os.path.dirname(os.path.realpath(__file__))
        self.upload_folder = os.path.join(os.getcwd(),"web/static/upload")
        self.output_folder = os.path.join(os.getcwd(),"web/static/output")
        self.SAMPLING_RATE = 16000
        self.use_onnx = False
        #初始化model和工具类
        #TODO 应该是一个单线程的处理，看看这个model是否支持多线程操作
        self.model = init_jit_model(os.path.join(os.path.dirname(os.path.realpath(__file__)),'files/silero_vad.jit'))

    def fotmat2Wav(self,output_folder, voice_list):
        # TODO 正则匹配下文件名是否是以wav为后缀的，不是的话，转换成wav
        # 创建input和output文件夹
        # ouput_folder = os.path.join(source_folder, "output")
        # 截取文件名
        wav_list = []
        if not os.path.exists(output_folder):
            print("output文件夹不存在")
            os.mkdir(output_folder)
        # 判断文件是否是mp3或者是m4a，然后转换成wav
        for item in voice_list:
            wav_name = item.split("\\")[-1].split(".")[0]
            print(item)
            print(wav_name)
            sound = AudioSegment.from_file(item)
            sound_len = sound.duration_seconds
            sound.export("%s.wav" % (wav_name), format="wav")
            wav_list.append("%s.wav" % (wav_name))
        return wav_list,sound_len

    def split_audio_by_energy(audio, min_silence_len=1000, silence_thresh=-50, energy_thresh=200):
        samples = np.array(audio.get_array_of_samples())
        samples = samples.astype(np.float32) / np.iinfo(samples.dtype).max
        samples = np.abs(samples)
        energy = np.convolve(samples, np.ones(min_silence_len), mode='valid')
        silence_mask = energy < energy_thresh
        split_points = np.where(np.diff(silence_mask.astype(np.int)) == 1)[0] + min_silence_len // 2
        split_points = np.concatenate(([0], split_points, [len(samples)]))
        audio_chunks = [audio[start:end] for start, end in zip(split_points[:-1], split_points[1:])]
        return audio_chunks

    def denoise(self,wav_file_path):
        print("开始去除背景的噪音...")
        print(wav_file_path)
        #加载噪音样本，让模型去掉目标文件里面类似的噪音
        noise_data, sample_rate = sf.read(os.path.join(self.cur_path,'noise.wav'))
        noise_data = noise_data.astype('float32')
        audio = AudioSegment.from_file(wav_file_path, format='wav')
        #转换成单声道
        # audio = audio.set_channels(1)
        # audio_chunks = split_on_silence(
        #     audio,
        #     min_silence_len=500,  # 最小静默长度
        #     silence_thresh=-50,  # 静默判定阈值
        #     keep_silence=500  # 拆分后保留的静默长度
        # )
        audio_chunks = audio[::2000]
        for i, chunk in enumerate(audio_chunks):
            # 应用噪音消除算法
            # chunk_array = chunk.get_array_of_samples()
            chunk_array = nr.reduce_noise(audio_clip=chunk, noise_clip=noise_data, verbose=False)
            chunk = chunk._spawn(chunk_array)
            # 保存音频片段
            chunk.export(f"audio_chunk_{i}.wav", format="wav")
        #分片
        # output_audio = audio_chunks[0]
        # for i in range(1, len(audio_chunks)):
        #     output_audio += audio_chunks[i]
        # output_audio.export('output_result.wav', format='wav')
        # noise_clip = noise_data[0:sample_rate]
        # noise_profile = get_noise(noise_clip,sample_rate)
        #TODO 单语音文件太大了，需要把分片处理后再合成一整个完整的语音

        # data,sample_rate  = sf.read(wav_file_path)
        # reduced_noise = reduce_noise(audio_clip=data, noise_clip=noise_data[0:sample_rate], verbose=False)
        # sf.write(wav_file_path,reduced_noise,sample_rate)
        print("噪音去除完成...")

    #开始对指定语音文件进行分析抽取
    def start(self,filepath):
        print("转换语音格式中....")
        source_path = os.path.join(self.upload_folder, "%s" % filepath)
        #源文件需要转化成wav格式
        source_file_stats = os.stat(source_path)
        print("将要识别的源文件%s :%d byte"%(source_path,source_file_stats.st_size))
        #TODO 暂时是只识别一个，后面可以是一整个列表
        voice_list = []
        voice_list.append(source_path)
        wav_list,sound_len = self.fotmat2Wav(self.output_folder,voice_list)
        print("文件的时长：%d",sound_len)
        print(wav_list)
        print("格式转换完毕.")
        start_time = time.time()
        for wav_file in wav_list:
            # TODO 需要一个取出杂音的步骤
            wav_stats = os.stat(wav_file)
            print("wav file size = %d"%wav_stats.st_size)
            wav = read_audio('%s' % wav_file, sampling_rate=self.SAMPLING_RATE)
            # get speech timestamps from full audio file
            st = get_speech_timestamps(wav, self.model, sampling_rate=self.SAMPLING_RATE, threshold=0.8)
            pprint(st)
            voice_section = []
            for i in range(len(st) - 1, -1, -1):
                #把太局促的声音片段给切掉，一般都是杂声，一半说话的都是连续的
                if(st[i]['end']-st[i]['start']<10000):
                    st.pop(i)
                    continue
                voice_section.append([st[i]['start']/self.SAMPLING_RATE/sound_len,st[i]['end']/self.SAMPLING_RATE/sound_len])
                print("开始-结束-总帧数：%d - %d - %d"%(st[i]['start'],st[i]['end'],st[i]['end']-st[i]['start']))

            #因为采样率是16000,所以1s对应的时间戳就是16000，2s的位置就是32000，以此类推，换算出所有片段对应的占整个音频的百分比数值
            print("片段中有人声的部分区间的百分比：")
            #存到数据库里面
            print(voice_section)
            print("保存合成录音")
            target_path = os.path.join(self.output_folder, "%s" % wav_file)
            print("target_path = %s" % target_path)
            fuck = collect_chunks(st, wav)
            save_audio(target_path, fuck, sampling_rate=self.SAMPLING_RATE)
            print("获取到人声在语音的位置")
            Audio(target_path)
            print("转换语音成功：%s 耗时：%d s" % (target_path, time.time() - start_time))
            #把生成的数据添加到数据库中
            saveVoiceRecord(filepath,sound_len,voice_section)
            # stream流下载到浏览器
            send_file(target_path, as_attachment=True)
            start_time = time.time()

