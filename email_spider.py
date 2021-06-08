from subdomain import bing_search
import sys
import getopt
import requests
from bs4 import BeautifulSoup
import re

def start(argv):
    url = ''
    pages = ''
    if len(sys.argv) < 2:
        #判断参数，如果少于两个,提示   
        print("-h 显示帮助信息;\n")
        sys.exit()
        #退出程序
    try:
        banner()
        #此函数用来刚开始显示的
        opts,arg=getopt.getopt(argv,"-u:-p:-h")
        #从命令行里获取到 -u -p -h 的值
    except getopt.GetoptError:
        print('错误参数')
        sys.exit()
    for opt,arg in opts:
        if opt == '-u':
            url = arg #将u后面的参数传入
        elif opt == '-p':
            pages = arg#将p后面的参数传入
        elif opt == '-h':
            print(usage())#
    # url = input('请输入网址  【例如:www.baidu.com】  ：')
    # pages = input('请输入爬行页数  【例如5】  :  ')
    launcher(url,pages)

def launcher(url,pages): #设置回调函数
    email_num = [] 
    key_words = ['email','mail','mailbox','邮箱','邮件','postbox']#设置关键字列表
    for page in range(1,int(pages)+1): #循环页数   
        for key_word in key_words: #循环关键词
            bing_email = bing_search(url,page,key_word) #调用bing_search 搜索
            baidu_email = baidu_search(url,page,key_word) #调用百度——search搜索
            sum_emails = bing_email + baidu_email #将所有结果汇总到一起
            for email in sum_emails: #遍历email
                if email in email_num:#如果存在，啥都不干
                    pass
                else:
                    print(email)#不存在了列表中，打印其，并且写入文件
                    with open('data.txt','a+') as f:
                        f.write(email+'\n')
                    email_num.append(email)#加入到列表
def search_email(html):#正则判断邮箱
    emails=re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[comxyz]+",html,re.I)
    return emails

def headers(referer):#定义请求头
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip,deflate',
    'Referer': referer
    }
    return headers

def bing_search(url,page,key_word):#定义bing搜素
    referer = "http://cn.bing.com/search?q=email+site%3abaidu.com&qs=n&sp=-1&pq=emailsite%3abaidu.com&first=1&FORM=PERE1"#设置referer字段
    conn = requests.session()#建立session连接
    bing_url = "http://cn.bing.com/search?q="+key_word+"+site%3a"+url+"&qs=n&sp=-1&pq="+key_word + "site%3a"+url+"&first="+str((page-1)*10)+"&FORM=PERE1" #bing搜索的url
    conn.get('http://cn.bing.com',headers=headers(referer))#请求一次bing获取cookie
    r = conn.get(bing_url,stream=True,headers=headers(referer),timeout=8)#发起请求
    emails =search_email(r.text) #进行正则进行匹配
    return emails

def baidu_search(url,page,key_word):#定义百度搜索
    email_list = [] 
    emails = []
    referer = "https://www.baidu.com/s?wd=email+site%3Abaidu.com&pn=1"#设置referer头
    baidu_url = "https://www.baidu.com/s?wd="+key_word+"+site%3A"+url+"&pn="+str((page-1)*10)#设置百度请求的url
    conn = requests.session()#发起session请求
    conn.get(referer,headers=headers(referer))#发起get请求，带上referer
    r = conn.get(baidu_url,headers=headers(referer))#发起get请求，带上header
    soup = BeautifulSoup(r.text,'lxml') #实例化返回结果
    tagh3 = soup.find_all('h3') 
    for h3 in tagh3:
        href = h3.find('a').get('href')
        try:
            r = requests.get(href,headers=headers(referer))
            emails = search_email(r.text)
        except Exception as e:
            pass
        for email in emails:
            email_list.append(email)
    return email_list

def banner():
    print('本工具由dcbygsec制作')
    print('本工具收集到的邮箱仅供参考，具体以实际测试为主')

def usage():
    print('-h: --help 帮助;')
    print('-u: --url 域名;')
    print('-p: --page 页数;')
    print('eg: python -u "www.baidu.com" -p 100' +'\n')
    sys.exit()

if __name__ == '__main__':
    try:
        start(sys.argv[1:])#传入自身文件名以外的参数
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")

