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


