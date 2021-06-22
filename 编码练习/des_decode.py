from Cryptodome.Cipher import DES
import binascii
key = b'abcdefgh' #key的密钥
des = DES.new(key,DES.MODE_ECB) #ecb模式
encryptResult = b'b81fcb047936afb76487dda463334767'
encrypto_text = binascii.a2b_hex(encryptResult)
decryptResult = des.decrypt(encrypto_text)
print(decryptResult)