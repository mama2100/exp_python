from Cryptodome.Cipher import AES
import binascii
key = b'abcdefghabcdefgh'
encryResult = b'51d23f9cab201da377c925ac526c4901' 
aes = AES.new(key,AES.MODE_ECB)
encrypto_text = binascii.a2b_hex(encryResult)
decrytResult = aes.decrypt(encrypto_text)
print(decrytResult)