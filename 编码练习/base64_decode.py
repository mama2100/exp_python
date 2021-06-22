import base64
bs = 'bXMwODA2Nw=='
bbs = str(base64.b64decode(bs),"utf-8")
print(bbs)