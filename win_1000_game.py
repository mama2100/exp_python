import logging #Python内置的标准模块，主要用于输出运行日志
import telnetlib #提供一个实现Telnet协议的类 Telnet
import time
import re

def main():
    try:
        tn = telnetlib.Telnet('192.168.56.122',port=1337) #发起telnet连接
    except:
        logging.warning("error") #如果登录失败弹出error
    time.sleep(0.5) #间隔0.5秒
    loop=1 #设置初始值为1
    while loop < 1002:
        data = tn.read_very_eager().decode('ascii')  #read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        print(data)
        res = re.search('(.*?)\s>',data).group(1) # 获取计算内容
        datas = calc(res) #调用计算函数进行计算
        print(str(loop)+":"+datas) #打印出每次结果
        loop=loop+1
        tn.write(datas.encode('ascii')+b"\n") #将计算结果以ascii码写入tenet连接，并且换行
        time.sleep(0.1)
    data = tn.read_very_eager().decode('ascii')#循环完成获取连接返回内容
    print(data)


def calc(res):#计算函数
    num1=res[1]
    num2=res[9]
    orperator =res[5]
    result = eval(num1+orperator+num2)
    return str(result)


main()

