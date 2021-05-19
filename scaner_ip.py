import socket
from whois import whois
def get_ip(domain):
    ip =socket.gethostbyname(domain)
    return ip

print(get_ip('www.baidu.com'))

data = whois('www.baidu.com')
print(data)