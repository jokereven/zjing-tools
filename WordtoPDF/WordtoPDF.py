import os

from win32com import client

'''
代码描述：
用来实现word文档转pdf的一个软件

特色：
可穿透指定路径下的所有文件，对找到的所有word文档进行操作
并把结果输出到指定路径中

注意事项：
请确认没有同名文件，否则文件会覆盖
'''

# 转换doc为pdf
def doc2pdf(fn):
    word = client.Dispatch("Word.Application")  # 打开word应用程序
    doc = word.Documents.Open(fn)  # 打开word文件

    a = os.path.split(fn)  # 分离路径和文件
    b = os.path.splitext(a[-1])[0]  # 拿到文件名

    doc.SaveAs("{}\\{}.pdf".format(path1, b), 17)  # 另存为后缀为".pdf"的文件，其中参数17表示为pdf
    doc.Close()  # 关闭原来word文件
    word.Quit()


# 转换docx为pdf
def docx2pdf(fn):
    word = client.Dispatch("Word.Application")  # 打开word应用程序
    doc = word.Documents.Open(fn)  # 打开word文件

    a = os.path.split(fn)  # 分离路径和文件
    b = os.path.splitext(a[-1])[0]  # 拿到文件名

    doc.SaveAs("{}\\{}.pdf".format(path1, b), 17)  # 另存为后缀为".pdf"的文件，其中参数17表示为pdf
    doc.Close()  # 关闭原来word文件
    word.Quit()


# 获取指定路径下的所有word文件
# 可以穿透指定路径下的所有文件
def getfile(path):
    word_list = []  # 用来存储所有的word文件路径
    for current_folder, list_folders, files in os.walk(path):
        for f in files:  # 用来遍历所有的文件，只取文件名，不取路径名
            if f.endswith('doc') or f.endswith('docx'):  # 判断word文档
                word_list.append(current_folder + '\\' + f)  # 把路径添加到列表中
    return word_list  # 返回这个word文档的路径


if __name__ == '__main__':
    word_path = input('[+] 请给出word文档所在路径：')

    # 设置一个路径path1，保存输出结果
    print("[+] 请输入一个路径，用来存放所有的处理结果")
    print("[+] 或者按回车键，我将自动把处理之后的文件存放在你的桌面")
    path1 = input('')  # path1 用来存放所有的处理结果
    if len(path1):
        pass
    else:
        desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')  # 获取桌面路径
        path1 = os.path.join(desktop_path, '所有的处理结果')
        os.makedirs(path1)

    print('[+] 转换中，请稍等...')
    words = getfile(word_path)
    for word in words:
        if word.endswith('doc'):
            doc2pdf(word)
        else:
            docx2pdf(word)
    print('[+] 转换完毕')
