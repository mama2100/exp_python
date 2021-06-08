import socket,sys
host = '127.0.0.1'
port = 6666
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#使用ipv4的tcp/ip连接
try:
    s.connect((host,port))
    #尝试连接目标端口
except Exception as e:
    print('server not found!')
    sys.exit()#退出程序
while True:
    c = input('You say:')
    s.sendall(c.encode())#编码发送
    data = s.recv(1024)#接收字符
    data =data.decode()#解码数据
    print('Received:',data)
    if c.lower() =='再见':
        break