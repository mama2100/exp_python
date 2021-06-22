from Cryptodome.Cipher import AES
import binascii
key = 'abcdefghabcdefgh'
text = 'ms08067'
text = text + (16 - (len(text) %16)) * '='
aes = AES.new(key,AES.MODE_ECB)#ecb模式
encrypto_text = aes.encrypt(text.encode())
encryptoResult = binascii.b2a_hex(encrypto_text)
print(text)
print(encryptoResult)