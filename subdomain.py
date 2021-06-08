#! /usr/bin/env python
#coding:utf-8
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse #此模块是用来解析url的
import sys

def bing_search(site,pages):
    Subdomain = []
    headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x8664; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'referer': "http://cn.bing.com/search?q=email+site%3abaidu.com&qs=n&sp=-1&pq=emailsite%3abaidu.com&first=2&FORM=PERE1"
    }
    for i in range(1,int(pages)+1):
        url = "https://cn.bing.com/search?q=site%3a"+site+"&go=Search&qs=ds&first="+ str((int(i)-1)*10) +"&FORM=PERE"
        conn = requests.session()#建立一个session连接
        conn.get('http://cn.bing.com',headers=headers)#先请求bing官网
        html = conn.get(url,stream=True,headers=headers,timeout=8)
        #当把get函数的stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载。需要注意一点：文件没有下载之前，它也需要保持连接。
        
        soup = BeautifulSoup(html.content,'html.parser')#使用html.parser解析器
        job_bt = soup.findAll('h2')#找到h2标签
        for i in job_bt:
            try:
                link = i.a.get('href')#找到其中的href的值
                domain = str(urlparse(link).scheme+"://"+urlparse(link).netloc) # urlparse() 解析URL
                #只要前面的协议和后面的主机名
                if domain in Subdomain:
                    pass
                else:
                    Subdomain.append(domain)
                    print(domain)    
            except:
                print('暂未搜索到结果')

if __name__ == '__main__':
    if len(sys.argv) == 3:
        site = sys.argv[1]
        page = sys.argv[2]
    else:
        print("usage:%s baidu.com 10"%sys.argv[0])
        sys.exit(-1)
    Subdomain = bing_search(site,page)
    

