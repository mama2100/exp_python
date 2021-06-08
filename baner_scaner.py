#!/usr/bin/python
#!coding:utf-8
from optparse import OptionParser #生成命令行参数
import time #产生延迟时间
import socket#产生tcp请求
import re#导入正则表达式模块

SIGNS = (
# 协议 | 版本 | 关键字
b'FTP|FTP|^220.*FTP',
b'MySQL|MySQL|mysql_native_password',
b'oracle-https|^220- ora',
b'Telnet|Telnet|Telnet',
b'Telnet|Telnet|^\r\n%connection closed by remote host!\x00$',
b'VNC|VNC|^RFB',
b'IMAP|IMAP|^\* OK.*?IMAP',
b'POP|POP|^\+OK.*?',
b'SMTP|SMTP|^220.*?SMTP',
b'Kangle|Kangle|HTTP.*kangle',
b'SMTP|SMTP|^554 SMTP',
b'SSH|SSH|^SSH-',
b'HTTPS|HTTPS|Location: https',
b'HTTP|HTTP|HTTP/1.1',
b'HTTP|HTTP|HTTP/1.0',)

def main():
    parser = OptionParser("Usage:%prog -i <target host> ") # 输出帮助信息
    parser.add_option('-i',type='string',dest='IP',help='specify target host')#获取ip地址参数
    parser.add_option('-p',type='string',dest='PORT',help='specify target host')#获取端口参数
    options,args = parser.parse_args()#对传进来的参数进行解析
    ip = options.IP#ip赋值
    port = options.PORT#端口赋值
    print("Scan report for "+ip+"\n")
    for line in port.split(','):#遍历扫描出的端口
        request(ip,line)#调用request函数
        time.sleep(0.2)
    print("\n Scan finished !  \n")

def request(ip,port):
    response = ''
    PROBE = 'GET / HTTP/1.0\r\n\r\n'#设置请求头
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#发起tcp的ipv4socket流连接
    sock.settimeout(10)#设置超时时间
    result = sock.connect_ex((ip,int(port)))#发起sock连接，这个是有返回值的
    if result == 0:
        try:
            sock.sendall(PROBE.encode())# 尝试发送string的所有数据， 成功则返回None， 失败则抛出异常。
            response = sock.recv(256) #接收数据此时指定接收的大小256字节
            if response: #如果有返回值
                regx(response,port)#使用正则将端口匹配出来
        except(ConnectionResetError,socket.timeout):#报错或者超时，忽略
            pass 
    else:
        pass
    sock.close()#关闭连接

def regx(response,port):
    text = ""
    if re.search(b'<title>502 Bad Gateway', response):#进行筛选，如果出现502
        proto = {"Service failed to access!!"}
    for pattern in SIGNS:#如果在协议中
        pattern = pattern.split(b'|')#提取出来
        if re.search(pattern[-1],response,re.IGNORECASE):
            proto = "["+port+"]"+"open"+pattern[1].decode()
            break
        else:
            proto = "["+port+"]"+"open " +pattern[1].decode()
    print(proto)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")

