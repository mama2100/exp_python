#!/usr/bin/python3
import os
import re
import optparse
from socket import timeout
from scapy.all import *

def HostAddress(iface):
    ipData = os.popen('ifconfig '+iface)#从一个命令打开一个管道 iface指的是网卡
    dataLine = ipData.readlines()#将读取到的数据一行一行读取出来
    #对ipData进行类型转换，再用正则进行匹配
    if re.search('\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',str(dataLine)):
        MAC = re.search('\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',str(dataLine)).group(0)#mac地址的正则匹配
        if re.search(r'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)',str(dataLine)):
            IP = re.search(r'((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)',str(dataLine)).group(0)
            #ip地址的正则匹配
        addressIndo=(IP,MAC)#返回一个元祖
    return addressIndo

def ArpScan(iface='ens33'):
    mac = HostAddress(iface)[1]   
    ip = HostAddress(iface)[0]
    #取出本地ip地址 
    ipSplit = ip.split('.')#对于本机的ip地址进行分割并作为依据元素，用于生成需要扫描的ip地址
    ipList=[]#需要扫描的ip地址列表
    for i in range(1,255):
        ipItem = ipSplit[0]+'.'+ipSplit[1]+'.'+ipSplit[2]+'.'+str(i)
        ipList.append(ipItem)
        """
            发送ARP
            因为要用到osi的二层和三层，所以要写成Ether/ARP
            最底层用了二层，所以要用srp（）发包
        """
    result = srp(Ether(src=mac,dst='FF:FF:FF:FF:FF:FF')/ARP(op=1,hwsrc=mac,hwdst='00:00:00:00:00:00',pdst=ipList),iface=iface,timeout=2,verbose=False)
        #srp()发送二层数据包，等待接收一个或者多个数据包的响应
        #Ether()以太网包，src表示目标主机,dst表示广播地址，arp表示arp包，op表示数量，hwsrc目标机器的mac地址，hwdst是我们自身的mac地址
       
    resultAns = result[0].res#读取result中的应答包和应答包内容
    liveHost=[]#存活主机列表
    number = len(resultAns)#取结果长度
    print('======================')
    print("ARP探测结果")
    print('本机ip地址:'+ip)
    print('本机的MAC地址：'+mac)
    print('======================')
    for x in range(number):
        IP = resultAns[x][1][1].fields['psrc']#取出其中ip的值
        MAC = resultAns[x][1][1].fields['hwsrc']#去处其中mac的值
        liveHost.append([IP,MAC])#将ip和mac组成列表添加到存活主机列表
        print("IP:"+IP+"\n\n"+"MAC:"+MAC)
        print('=======================')
    resultFile=open('result','w')#打开文件
    for i in range(len(liveHost)):#将存活列表遍历出来
        resultFile.write(liveHost[i][0]+'\n')
    resultFile.close()
if __name__ == '__main__':
    parser = optparse.OptionParser('usage: python %prog -i interfaces \n\n'
                                    'Example: python %prog -i eth0\n')
    #添加说明
    parser.add_option('-i','--iface',dest='iface',default='eth0',type='string',help='interfaces name')#添加网卡参数
    (options, args) = parser.parse_args()#实例化输入的函数
    ArpScan(options.iface)
