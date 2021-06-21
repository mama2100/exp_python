from urllib.error import URLError
from urllib.request import ProxyBasicAuthHandler, ProxyHandler, build_opener

proxy = "127.0.0.1:1181"#代理地址
proxy_handler = ProxyHandler({
    'http':'http://'+proxy,
    'https':'https://'+proxy
})
opener=build_opener(proxy_handler)
try:
    response = opener.open('http://httobin.org/get')#测试IP的网址
    print(response.read().decode('utf-8'))
except URLError as e:
    print(e.reason)