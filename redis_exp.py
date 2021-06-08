import socket #建立tcp连接
import sys #调用系统包

PASSWORD_DIC=['redis','root','oracle','password','p@aaw0rd','abc123!','123456','admin'] #密码列表

def check(ip,port,timeout): #检查是否存在函数
    try:
        socket.setdefaulttimeout(timeout)#设置超时时间
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#发起tcp请求
        s.connect((ip,int(port)))#发起tcp链接
        s.send("INFO\r\n")#发送数据
        result = s.recv(1024) #接受返回数据
        if "redis_version" in result:
            return u'存在未授权访问'
        elif "Authentication" in result:#如果存在认证
            for pass_ in PASSWORD_DIC:#遍历密码
                s =socket.socket(socket.AF_INET,socket.SOCK_STREAM)#发起tcp请求
                s.connect((ip,int(port)))#发起tcp链接
                s.send("AUTH %s\r\n" %(pass_))#发送数据
                result = s.recv(1024)#接受返回数据
                if '+OK' in result:
                    print("存在弱口令，密码：%s"%pass_)
    except Exception as e:
        pass

if __name__ == '__main__':
    ip=sys.argv[1]
    port=sys.argv[2]
    print(check(ip,port,timeout=10))
    