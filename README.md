# 盲猜派RLE
基于位层面RLE实现对文件的加密

对文件中B个字节进行位层面RLE，间隔A个字节不作处理，总计进行n次。

A B n 将进行一定的变换，作为密钥。解密时需要输入密钥。

###位层面RLE：

依次记录连续的0和1（1和0，依文件第一个字符而定）的出现数量， 转换为二进制后写入文件。


