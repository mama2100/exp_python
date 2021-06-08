import requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0"
}
url = input("url: ")
txt = input('请选择打开的字典文件：（默认php.txt）')
url_list = []
if txt == "":
    txt = "php.txt"

try:
    with open(txt,'r') as f:
        for a in f:
            a = a.replace('\n','')
            url_list.append(a)
        f.close()
except:
    print("error!")

for li in url_list:
    conn = "http://"+url+"/"+li
    try:
        response = requests.get(conn,headers=headers)
        result = conn+'--------------'+str(response)
        print(result)
        with open('result.txt','a+') as fp:
            fp.writelines(result)
    except Exception as e:
        print(e,'error')