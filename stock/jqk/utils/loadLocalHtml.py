# 打开文件并读取内容
def loadLocalHtml(path, encoding='utf-8') -> str:
    with open(path, 'r', encoding=encoding) as file:
        data = file.read()

    # 现在 data 变量包含了 temp.html 文件的所有内容
    # print(data)
    print('load file end from local')
    return data
