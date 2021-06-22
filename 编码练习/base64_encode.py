import base64
s = 'ms08067'
bs =base64.b64encode(s.encode("utf-8"))
print(bs)