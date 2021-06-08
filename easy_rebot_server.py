import socket
language={'what is your name':'I am Tom','how old are you':'25','bye':'bye!'}
host = '127.0.0.1'
port = 6666
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #网络使用ipv4，协议选择tcp连接
s.bind((host,port)) #绑地址端口
s.listen(1) #将socket设置成监听模式，可以监听backlog外来的连接请求，最大请求数为1
print('listening at port 6666')
conn,addr = s.accept()#返回一个客户机socket，带有客户机端的地址信息。
# accept方法返回一个双元素元组，形如(connection,address)。第一个元素是新的socket对象，第二个元素是客户的IP地址
print('Connect by:',addr)
while True:
    data = conn.recv(1024)#从socket中接收数据，最多接收buflen个字符，一般填写1024个
    data = data.decode()#对socket数据进行解码
    if not data: #判断数据如果不存在
        break
    print('received message:',data)
    conn.sendall(language.get(data,'Nothing').encode())
    #发送指定数据，如果在字典中，则返回对应的值，如果不在，则返回nothing，并进行编码
conn.close()#关闭客户机socket
s.close()#关闭服务器socket