from Cryptodome.Cipher import DES
import binascii
key = b'abcdefgh' #key的长度需为8字节
des = DES.new(key,DES.MODE_ECB) #ecb模式
text = 'ms08067.com' #加密文字
text = text + (8-(len(text) %8)) * '=' #11%8=3
encrypt_text = des.encrypt(text.encode()) #进行加密
encryptResult = binascii.b2a_hex(encrypt_text)#返回16进制字符串
print(text)
print(encrypt_text)
print(encryptResult)