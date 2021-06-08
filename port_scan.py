#coding:utf-8
import sys
import socket
import optparse
import threading
import queue

"""
1.重写threading.Thread方法，把需要传递的参数，全部传进来，这里需要传入端口队列，目标ip，以及探测超时时间
2.加入run方法，传入self  写一个循环，判断队列是否为空，空及说明扫描完毕，跳出循环，然后取出端口，设置超时时间为0.5s
3.发起socket连接，设置超时时间为0.5s，进行连接，这里使用connect_ex，和connect的区别在于有返回值
4.进行判断，有返回值说明端口开放
5.关闭连接
6.定义一个开始扫描函数，传入ip，端口范围，线程数
7.设置一个列表，用于存放端口，
8.进行判断，如果端口参数中有-，则通过for循环，将其的所有范围取出来，加入到列表里，如果没有，表面扫描一个端口
9.目标ip从命令行参数获取，线程数，生成队列
10.将端口写入队列
11.将任务加入线程池
12.启动线程，阻塞线程
"""

class PortScaner(threading.Thread):
    def __init__(self,portqueue,ip,timeout=3):#需要传入端口队列，目标ip，探测超时时间
        threading.Thread.__init__(self)
        self.__portqueue = portqueue
        self.__ip = ip
        self.__timeout=timeout
    def run(self):
        while True:
            if self.__portqueue.empty():#判断队列是否为空
                break#端口列表为空，说明已经扫描完毕，跳出循环
            port = self.__portqueue.get(timeout=0.5)#从端口列表中取出端口，超时时间为0.5s
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)#发起socket连接,socket.SOCK_STREAM　　流式socket , for TCP (默认)
                s.settimeout(self.__timeout)#设置超时时间
                result_code = s.connect_ex((self.__ip,port))#连接到address处的套接字。只不过有返回值
                if result_code == 0:
                    sys.stdout.write(("[%d] OPEN\n" %port))
            except Exception as e:
                print(e)
            finally:
                s.close()
def StartScan(targetip,port,threadNum):
    portList = [] #端口列表
    if '-' in port:
        for i in range(int(port.split('-')[0]),int(port.split('-')[1])+1):
                    #判断是单个端口还是范围端口
            portList.append(i)
    else:
        portList.append(int(port))

    ip=targetip#目标ip地址
    threads=[]#线程池
    threadNumber=threadNum#线程数
    portQueue=queue.Queue()#创建队列
    for port in portList:
        portQueue.put(port)#将端口写入队列，timeout等待时间 
    for t in range(threadNumber):
        threads.append(PortScaner(portQueue,ip,timeout=3))#将任务加入线程池
    for thread in threads:
        thread.start()#启动线程
    for thread in threads:
        thread.join()#阻塞线程

if __name__ == '__main__':
    parser = optparse.OptionParser('Example: python %prog -i 127.0.0.1 -p 80 \n python %prog -i 127.0.0.1 -p 1-100\n')#实例化并添加说明
    parser.add_option('-i','--ip',dest='targetIP',default='127.0.0.1',type='string',help='target IP')
    #添加ip参数-i
    parser.add_option('-p','--port',dest='port',default='80',type='string',help='scann port')#添加端口参数-p
    parser.add_option('-t','--thread',dest='threadNum',default='100',type='int',help='scann thread number')#添加端口参数-p
    (options,args) = parser.parse_args()#对传入进来的参数进行解析
    StartScan(options.targetIP, options.port, options.threadNum)
    #开始扫描   