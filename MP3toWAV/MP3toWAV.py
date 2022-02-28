import os
import shutil

import pydub
from pydub import AudioSegment

"""
第一 你需要python的环境
其次 你需要一个编辑器
```
这里比较推荐 vscode和pychorm
```
最后 你需要有ffmpeg的环境
[ffmpeg下载与环境配置](https://zhuanlan.zhihu.com/p/324472015)
 """


# mp3 or wav
type = input("mp3 or wav:")
# 文件所在位置
FileDir = input("Please enter the folder where the file resides:")
# 获取当前path
NowPath = os.getcwd()
# 获取桌面path
desk = os.path.join(os.path.expanduser("~"), 'Desktop') + '\\'


# mp3 -> wav
def Mp3ToWav(FilePath):
        for i in FilePath:
            song = AudioSegment.from_mp3(i)
            Filename = i.split("\\")[len(i.split('\\'))-1].split(".mp3")[0]
            song.export(Filename+".wav", format="wav")

# wav -> mp3
def WavToMp3(FilePath):
        for i in FilePath:
            sound = pydub.AudioSegment.from_wav(i)
            MusicName = i.split("\\")[len(i.split("\\"))-1].split(".wav")[0]
            sound.export(NowPath+"\\"+MusicName+".mp3", format="mp3")

# 获取指定路径下的所有mp3|wav文件
def getfile(FileDir):
    mp3_list = []  # 用来存储所有的mp3文件路径
    wav_list = []
    for current_folder, list_folders, files in os.walk(FileDir):
        for f in files:  # 用来遍历所有的文件，只取文件名，不取路径名
            if f.endswith('mp3'):# 判断mp3文档
                mp3_list.append(current_folder + '\\' + f)  # 把路径添加到列表中
            if f.endswith('wav'):
                wav_list.append(current_folder + '\\' + f)  # 把路径添加到列表中
    Mp3ToWav(mp3_list)
    WavToMp3(wav_list)
    return mp3_list,wav_list# 返回这个mp3,wav文档的路径

# 处理mp3文件
def mp3(FileDir):
    getfile(FileDir)

# 处理wav文件
def wav(FileDir):
    getfile(FileDir)

if type == "mp3":
    mp3(FileDir)
elif type == "wav":
    wav(FileDir)
else:
    print("小兄弟想什么嘞")

def move():
    data_path = NowPath

    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.endswith("wav") | file.endswith("mp3"):
                old_file_path = os.path.join(root, file)
                new_path = desk+'//MP3toWAV/'
                if not os.path.exists(new_path):  # 创建新文件夹
                    os.makedirs(new_path)
                new_file_path = new_path + '/' + file
                print(new_file_path+"转换完成!!!")
                shutil.move(old_file_path, new_file_path) # 复制文件
move()
