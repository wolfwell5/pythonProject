import os
import sys
import time
import winreg
import struct

ten_thousand = 10000
one_hundred = 100
hex_val = 0xFFFFFF

# D:\Entertainment\同花顺\history\sznse\day

key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\HexinSoft")
hexinpath, type = winreg.QueryValueEx(key, "FilePath")  # 同花顺安装路径
# installdate, type = winreg.QueryValueEx(key, "InstallDate") # 安装日期
# print("同花顺安装路径：", hexinpath, "安装日期：", installdate)
print("同花顺安装路径：", hexinpath)
winreg.CloseKey(key)
daylines = []   # 股市列表
textpath = r"E:\Develop\Repos\tempFile"    #文本文件存储目录
shaseday = r"history\shase\day"     # 沪市日线路径
sznseday = r"history\sznse\day"     # 深市日线路径
# stbday = r"history\stb\day"         # 北京日线路径
daylines.append(shaseday)
daylines.append(sznseday)
# daylines.append(stbday)
# print(daylines)

if len(sys.argv)>1:
    today = str(sys.argv[1])    # 运行参数 （样式为YYYYMMDD,如20220301）
else:
    loctime=time.localtime(time.time())
    today = time.strftime("%Y%m%d",loctime) # 无运行参数，则默认为当天（样式为YYYYMMDD,如20220301）
    # today='19961101'
    from_today = '20250123'
    to_today = '20250127'
txtfile = os.path.join(textpath, today+".txt")  # 输出文本文件名

if os.path.exists(txtfile):
    os.remove(txtfile)      # 若文本文件存在则先删除
# print(txtfile, today)
for market in daylines:
    dayfilepath = os.path.join(hexinpath, market)   # 日线文件存储完整路径
    daylinefiles = os.listdir(dayfilepath)  # 日线文件名列表
    # print(txtfilepath, hexinpath)
    if len(daylinefiles) > 0:
        # print(len(daylinefiles))
        for dfn in daylinefiles:
            if ".day" in dfn:
                stkday = os.path.join(dayfilepath, dfn)
                (shotname, extension) = os.path.splitext(dfn)
                # txtfile = os.path.join(txtfilepath, shotname+".txt")
                # print(stkday,txtfile)
                binfile = open(stkday, 'rb')
                binfile.seek(6)
                recnums = struct.unpack('i', binfile.read(4))[0]    # 记录数
                recbgn = struct.unpack('h', binfile.read(2))[0]     # 记录开始地址
                reclen = struct.unpack('h', binfile.read(2))[0]     # 记录长度
                tf = open(txtfile,"a+")
                for i in range(recnums):
                    binfile.seek(recbgn + reclen * i)
                    stkdate = struct.unpack('I', binfile.read(4))[0]        # 日期
                    # if stkdate == int(today):
                    stkopen = (struct.unpack('I', binfile.read(4))[0] & hex_val) / ten_thousand    # 开盘价
                    stkhigh = (struct.unpack('I', binfile.read(4))[0] & hex_val) / ten_thousand    # 最高价
                    stklow = (struct.unpack('I', binfile.read(4))[0] & hex_val) / ten_thousand     # 最低价
                    stkclose = (struct.unpack('I', binfile.read(4))[0] & hex_val) / ten_thousand   # 收盘价
                    # money = round((struct.unpack('I', binfile.read(4))[0] & 0xFFFFFFF) * 100 / ten_thousand / ten_thousand, 2)  # 成交金额
                    money = (struct.unpack('I', binfile.read(4))[0] & 0xFFFFFFF)  # 成交金额
                    amount = round(struct.unpack('I', binfile.read(4))[0] / ten_thousand, 2)  # 成交量
                    # print(shotname, stkopen, stkhigh, stklow, stkclose, amount, money)
                    print(shotname + '\t', str(stkopen) + '\t', str(stkhigh) + '\t', str(stklow) + '\t', str(stkclose) + '\t',
                          str(amount) + '\t', str(money) + '\t', file=tf)  # 写入本文文件
                binfile.close()

tf.close()
print("文件输出完毕！")
