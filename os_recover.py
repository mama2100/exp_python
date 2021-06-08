#!coding:utf-8
from optparse import OptionParser #生成命令行参数
import os #执行系统命令
import re # 匹配返回的ttl值

def main():
    parser = OptionParser("Usage:%prog -i <target host> ")#输出帮助信息
    parser.add_option('-i',type='string',dest='IP',help='specify target host')#获取ip地址参数
    options,args=parser.parse_args()#实例化参数
    ip = options.IP#ip从命令行中获取
    ttl_scan(ip)#调用函数

def ttl_scan(ip):
    ttlstrmatch = re.compile(r'ttl=\d+')#筛选ttl=xx
    ttlnummatch = re.compile(r'\d+') #ttl数值内容
    result = os.popen("ping -c 1 "+ip)
    res = result.read()
    for line in res.splitlines():
        result = ttlstrmatch.findall(line)
        if result:
            ttl = ttlnummatch.findall(result[0])
            if int(ttl[0]) <= 64:#判断目标主机响应包中ttl的值是否小于等于64
                print("%s is Linux/Unix"%ip)#小于64为linx/unix系统
            else:
                print("%s is Windows"%ip)#反之则为windows系统
        else:
            pass
if __name__ == '__main__':
    main()
    