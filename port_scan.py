#coding:utf-8
import sys
import socket
import optparse
import threading
import queue

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
            port = self.__portqueue.get(timeout=0.5)#从端口列表中取出端口，超时时间为1s
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
    portNumb =port
    if '-' in port:
        for i in range(int(port.split('-')[0]),int(port.split('-')[1])+1):
                    #判断是单个端口还是范围端口
            portList.append(i)
    else:
        portList.append(int(port))

    ip=targetip#目标ip地址
    threads=[]#线程数量
    threadNumber=threadNum#端口队列
    portQueue=queue.Queue()#生成端口，加入端口队列
    for port in portList:
        portQueue.put(port)
    for t in range(threadNumber):
        threads.append(PortScaner(portQueue,ip,timeout=3))
    for thread in threads:
        thread.start()#启动线程
    for thread in threads:
        thread.join()#阻塞线程

if __name__ == '__main__':
    parser = optparse.OptionParser('Example: python %prog -i 127.0.0.1 -p 80 \n python %prog -i 127.0.0.1 -p 1-100\n')
    parser.add_option('-i','--ip',dest='targetIP',default='127.0.0.1',type='string',help='target IP')
    #添加ip参数-i
    parser.add_option('-p','--port',dest='port',default='80',type='string',help='scann port')#添加端口参数-p
    parser.add_option('-t','--thread',dest='threadNum',default='100',type='int',help='scann thread number')#添加端口参数-p
    (options,args) = parser.parse_args()
    StartScan(options.targetIP, options.port, options.threadNum)
    #开始扫描   