import random
import string
import struct


print("制作者：盲猜派高层")
print("版本：V0.1")
print("""该程序通过对文件进行位层面的RLE来实现加密，
由于位层面的RLE压缩率低下（约为300%），因此请酌情选择加密数据块大小。
输入的ABn越小，影响到的数据大小就越小，具体参见GitHub""")
print()


"""
打开文件
"""
print("可以直接将文件拖到窗口内（建议采用此种方法）")
codepath = input("要加密的文件（输入文件路径，需包括文件本身）：")
f = open(codepath, "rb") #打开文件
fw = open(codepath + ".bgsrle", "wb")  # 创建加密后的文件


"""
获得密钥数字
"""
print("请输入三个数字A,B,n")
print("A ∈ (0, 8192] 默认值1024")
print("B ∈ (0, 8192] 默认值1024")
print("n ∈ (0, 65536] 默认值1024")

A = input("A:")
try:
    A = int(A)
except ValueError as e:
    print("A已按默认值处理")
    A = 1024
if A < 1 or A > 8192:
    print("A已按默认值处理")
    A = 1024

B = input("B:")
try:
    B = int(B)
except ValueError as e:
    print("B已按默认值处理")
    B = 1024
if B < 1 or B > 8192:
    print("B已按默认值处理")
    B = 1024

n = input("n:")
try:
    n = int(n)
except ValueError as e:
    print("n已按默认值处理")
    n = 1024
if n < 1 or n > 65536:
    print("n已按默认值处理")
    n = 1024


"""
生成密钥
"""
bitLen = max(len(str(A)), len(str(B)), len(str(n)))
secKeyA = str(A) + 'P' * (bitLen - len(str(A)))
secKeyB = str(B) + 'P' * (bitLen - len(str(B)))
secKeyn = str(n) + 'P' * (bitLen - len(str(n)))
secList = [secKeyA[i] + secKeyB[i] + secKeyn[i] for i in range(bitLen)]
secKey = ""
charaList = string.ascii_letters
for i in secList:
    noneMeaningCharAmount = random.randint(0,8)
    noneMeaningCharList = random.choices(charaList, k=noneMeaningCharAmount)
    noneMeaningCharList = [j for j in noneMeaningCharList if j != 'P']
    noneMeaningStr = ""
    noneMeaningStr = noneMeaningStr.join(noneMeaningCharList)
    secKey += noneMeaningStr
    secKey += i



"""
变量定义
"""
processingCode = b""  # 当前要处理的数据块
processingByte = ""  # 当前正在处理的字节
firstCode = ''  # 数据块中的第一个字符
nowDot = firstCode  # 当前正在累积的字符
cnt = 0  # 计数器
numList = []  # 字符离前一串不同字符的位置
waitWrite = ""  # 将要写入文件的字节


"""
处理
"""
for iii in range(n):  # 总计n次读取 + 加密
    numList = []
    processingCode = f.read(B)
    if not processingCode:
        break

    firstCode = processingCode[0]
    firstCode = bin(firstCode)[2:]  # 去除0b
    firstCode = ('0' * (8-len(firstCode))) + firstCode  # 高位补0
    firstCode = firstCode[0]  # 取得第一个字符

    nowDot = firstCode

    for i in processingCode:
        processingByte = bin(i)
        processingByte = processingByte[2:]  # 去除0b
        processingByte = ('0' * (8-len(processingByte))) + processingByte  # 高位补0
        for z in processingByte:  # 枚举正处理的字节的每一位
            if z == nowDot:
                cnt += 1
            else:
                numList.append(cnt)
                cnt = 1
                nowDot = str(int(nowDot) ^ 1)
    numList.append(cnt)
    numList.append("STOP")
    cnt = 0

    # 写入加密后的数据
    if firstCode == '1':
        waitWrite = 255
    else:
        waitWrite = 0
    k = struct.pack(">B", waitWrite)  # 写入首位
    fw.write(k)

    i = 0
    while True:
        if numList[i] == "STOP":
            break
        waitWrite = numList[i]
        k = struct.pack(">B", waitWrite)
        fw.write(k)
        i += 1
        pass

    # 写入大小A字节的间隔字节
    blockBytes = f.read(A)
    fw.write(blockBytes)

# 写入剩余的所有字节
leftBytes = f.read()
fw.write(leftBytes)

f.close()
fw.close()

print("密钥：", secKey)
#代码结束


