print("制作者：盲猜派高层")
print("版本：V1.0b4") #1.0版本，以4bit为一个划分单元
print("""
该程序对经过盲猜派RLE1.0b4混淆后的文件进行解析，
你需要告知程序先前混淆时给定的长度，
程序不会判断文件，请确保输入程序的文件为混淆所得""")
print()

import struct


'''
读取区
'''
print("请选择混淆时给定的数据长度（128-1024 单位：B 默认：128 不在范围内的数据设为128）")
datalen = input()
try:
    datalen = int(datalen)
except:
    print("数据非数字 已按照默认值处理")
    datalen = 128
if datalen < 128 or datalen > 1024:
    datalen = 128

print()

print("可以直接将文件拖到窗口内（建议采用此种方法）")
codepath = input("要解析的文件（输入文件路径，需包括文件本身）：")
f = open(codepath, "rb") #打开文件


"""
处理区
"""
#创建解密后文件（空）
fw = open(codepath + ".bgsrleout", "wb")

flag = True
writelist = 0
bitcnt = 7 #7最高位 0最低位
cnt = 0 #写入了几个字节
wait_to_write = 0
#得首位
k = f.read(1)
k = bin(k[0])
if k[-1] == '1':
    nowdot = 1
else:
    nowdot = 0

while flag:
    nowcode = f.read(1)
    if not nowcode:
        break

    nowbit = bin(nowcode[0])

    nowbit = nowbit[2:] #删掉0b
    nowbit = ('0' * (8-len(nowbit))) + nowbit #补高位零

    #切分两段
    nowbit1 = nowbit[0:4]
    nowbit2 = nowbit[4:]

    #开始置0和1的数量 一共置两次
    flag2 = False
    pownum = 3
    ansnum = 0 #写入的数 md起个短点的变量名怎么那么难
    for z in nowbit1:
        ansnum += int(z) * (2 ** pownum)
        pownum -= 1
    if nowbit1 != '0000':
        writelist = ansnum
        flag2 = True
    #立刻写入
    while flag2:
        if bitcnt == -1:
            wait_to_write = struct.pack('B', wait_to_write)
            fw.write(wait_to_write)

            wait_to_write = 0
            bitcnt = 7

            cnt += 1
            if cnt >= datalen:
                flag = 0

        if writelist == 0:
            nowdot = 1 - nowdot #1变0 0变1
            break

        wait_to_write += (2 ** bitcnt) * nowdot
        writelist -= 1
        bitcnt -= 1

    #第二次
    flag2 = False
    pownum = 3
    ansnum = 0
    for z in nowbit2:
        ansnum += int(z) * (2 ** pownum)
        pownum -= 1
    if nowbit2 != '0000':
        writelist = ansnum
        flag2 = True
    #立刻写入
    while flag2:
        if bitcnt == -1:
            wait_to_write = struct.pack('B', wait_to_write)
            fw.write(wait_to_write)

            wait_to_write = 0
            bitcnt = 7

            cnt += 1
            if cnt >= datalen:
                flag = 0

        if writelist == 0:
            nowdot = 1 - nowdot #1变0 0变1
            break

        wait_to_write += (2 ** bitcnt) * nowdot
        writelist -= 1
        bitcnt -= 1



'''
收尾
'''
r = f.read()
fw.write(r)

f.close()
fw.close()


#代码结束



