print("制作者：盲猜派高层")
print("版本：V1.0b8") #1.0版本，以8bit为一个划分单元
print("""该程序通过对文件头部一定位数的数据进行位层面的RLE来实现混淆，
由于位层面的RLE压缩率低下（约为300%），因此无法实现压缩。
用户可自行选择处理的数据长度""")
print()

import struct

"""
读取区
"""
print("请选择需要处理的数据长度（128-1024 单位：B 默认：128 不在范围内的数据设为128）")
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
codepath = input("要混淆的文件（输入文件路径，需包括文件本身）：")
f = open(codepath, "rb") #打开文件


"""
预处理区
"""
numlist = [] #字符离前一串不同字符的位置
count = 0 #计数器

#创建加密后文件（空）
fw = open(codepath + ".bgsrle", "wb")

#录入第一个字符
firstcode = f.read(1) #是一个二进制格式的数
firstcode = bin(firstcode[0])[2:] #转为二进制写法（即0b多少多少）的字符串，但去除0b
firstcode = ('0' * (8-len(firstcode))) + firstcode #补零
firstcode = firstcode[0] #获取第一个字符
#当前字符 目前是第一个字符
nowdot = firstcode
#指针移回最开始
f.seek(0)


"""
处理区
"""
nowcode = f.read(datalen) #读取文件 这玩意1是1字节

#print(nowcode)
#用i遍历nowcode里面每一个二进制数 nowcode中的二进制数列并非是连续的，而是会因为某种规则而分成若干个8bit二进制数
for i in nowcode:
    nowbit = bin(i) #i转为二进制表示 0b…… 是个字符串！
    nowbit = nowbit[2:] #去除0b
    nowbit = ('0' * (8-len(nowbit))) + nowbit #补高位零
    for z in nowbit: #枚举每一位
        if z == nowdot: #如果z与当前字符相同
            count += 1 #计数+1
        else: #如果不相同
            numlist.append(count)
            count = 1
            nowdot = str(1 - int(nowdot)) #更换当前字符
numlist.append(count)


#结束标记
numlist.append("STOP")
#print(numlist)


"""
写入区
"""
if firstcode == '1': #首位为1
    waitwrite = 255
else: #首位为0
    waitwrite = 0

k = struct.pack(">B", waitwrite) #确定首位

fw.write(k)

i = 0  # 标记
while True: #一个为一个字节
    if numlist[i] == 'STOP':
        break
    waitwrite = numlist[i]
    #print(waitwrite,end=' ')
    k = struct.pack(">B", waitwrite)
    fw.write(k)

    i += 1
    pass



'''
写入剩余部分
'''
wowo = f.read()
fw.write(wowo)
f.close()
fw.close()


#代码结束
