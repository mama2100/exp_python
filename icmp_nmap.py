#coding:utf-8
import nmap
import optparse


def NampScan(targetIP):
    nm = nmap.PortScanner()
    # 实例化PortScanner对象
    try:
        #hosts为目标ip地址，argusments为nmap的扫描参数
        # -sn：使用ping进行扫描
        # -PE：使用icmp的echo请求包（-PP：使用timestamp请求包 -PM:netmask请求包）
        result = nm.scan(hosts=targetIP,arguments='-sn -PE')
        state = result['scan'][targetIP]['status']['state']#对结果进行切片，提取主机状态信息
        print("[{}] is [{}]".format(targetIP,state))
    except Exception as e:
        pass

if __name__ == '__main__':
    parser = optparse.OptionParser("usage: python %prog -i ip \n\n Example: python %prog -i 192.168.1.1 [192.168.1.1-100]\n")
    #实例化对象，传入用法
    parser.add_option('-i','--ip',dest='targetIP',default='192.168.1.1',type='string',help='target ip address')
    options,args=parser.parse_args()
    #判断是单台主机还是多台主机
    #ip中如果存在'-'，说明要扫描多台主机
    if '-' in options.targetIP:
        #代码举例：192.168.1.1-120
        #通过'-'进行分割，
        #把192.168.1.1通过“，”进行分割取最后一个数作为range函数的start，然后把120+1作为range函数的stop
        #这样循环遍历出需要扫描的ip地址
        for i in range(int(options.IP.split('-')[0].split('.')[3]),int(options.IP.split('-')[1])+1):
            NampScan(options.targetIP.split('.')[0]+'.'+options.targetIP.split('.')[1]+'.'+options.targetIP.split('.')[2]+'.'+str(i))
    else:
        NampScan(options.targetIP)