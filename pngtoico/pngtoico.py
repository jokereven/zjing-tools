import os
import tkinter as tk
from tkinter import filedialog

from PIL import Image

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

# 图标大小
size = (256,256)

# 分离文件名与扩展名
tmp = os.path.splitext(file_path)
# 因为python文件跟图片在同目录，所以需要判断一下
if tmp[1] == '.jpg' or tmp[1] == '.png':
    outName = tmp[0] + '.ico'
    # 打开图片并设置大小
    im = Image.open(file_path).resize(size)
    try:
        # 图标文件保存至icon目录
        path = os.path.join('icon', outName)
        im.save(path)

        print('{} --> {}'.format(file_path, outName))
    except IOError:
        print('connot convert :',file_path)
