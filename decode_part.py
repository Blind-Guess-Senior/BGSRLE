import struct


print("制作者：盲猜派高层")
print("版本：V0.1")
print("""
该程序对经过盲猜派RLE2.0加密后的文件进行解密，
你需要告知程序密钥，
程序不会判断文件，请确保输入程序的文件为加密所得""")
print()


"""
打开文件
"""
print("可以直接将文件拖到窗口内（建议采用此种方法）")
codepath = input("要解密的文件（输入文件路径，需包括文件本身）：")
f = open(codepath, "rb")  # 打开文件
fw = open(codepath + ".bgsrleout", "wb")


"""
解析密钥
"""
secKeyA, secKeyB, secKeyn = "", "", ""
A,B,n = 0,0,0
meaningSecChara = [str(i) for i in range(10)]
meaningSecChara.append('P')
print("输入密钥：")
secKey = input()
i = 0
while i < len(secKey):
    if secKey[i] in meaningSecChara:
        secKeyA += secKey[i]
        secKeyB += secKey[i + 1]
        secKeyn += secKey[i + 2]
        i += 3
    else:
        i += 1
        continue

for i in secKeyA:
    if i == 'P':
        break
    A *= 10
    A += int(i)
for i in secKeyB:
    if i == 'P':
        break
    B *= 10
    B += int(i)
for i in secKeyn:
    if i == 'P':
        break
    n *= 10
    n += int(i)

"""
变量定义
"""
processingByte = b''  # 当前正在处理的字节
firstCode = ''  # 第一个字符
nowDot = 1  # 当前正在累积哪个字符
bitCnt = 7  # 解密后字节写到第几位
cnt = 0  # 当前数据块解密了几个字节
powNum = 7  # 当前字符要放在第几位
waitWriteBitCnt = 0
waitWriteNum = 0


"""
处理区
"""
for iii in range(n):
    firstCode = f.read(1)
    if not firstCode:
        iii += 114514
        break
    firstCode = bin(firstCode[0])
    if firstCode[-1] == '1':
        nowDot = 1
    else:
        nowDot = 0

    cnt = 0
    while cnt < B:
        processingByte = f.read(1)
        if not  processingByte:
            break
        processingByte = bin(processingByte[0])[2:]
        processingByte = ('0' * (8-len(processingByte))) + processingByte  # 高位补零

        flag = True
        powNum = 7
        waitWriteBitCnt = 0
        for z in processingByte:
            waitWriteBitCnt += int(z) * (2 ** powNum)
            powNum -= 1
        if processingByte == '00000000':
            flag = False
        while flag:
            if bitCnt == -1:
                waitWriteByte = struct.pack("B", waitWriteNum)
                fw.write(waitWriteByte)

                waitWriteNum = 0
                bitCnt = 7

                cnt += 1

            if waitWriteBitCnt == 0:
                nowDot = nowDot ^ 1
                break

            waitWriteNum += (2 ** bitCnt) * nowDot
            waitWriteBitCnt -= 1
            bitCnt -= 1

    blockBytes = f.read(A)
    fw.write(blockBytes)


"""
收尾
"""
leftBytes = f.read()
fw.write(leftBytes)

f.close()
fw.close()

#代码结束



