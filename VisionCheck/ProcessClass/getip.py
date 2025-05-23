import socket
import netifaces as ni
import fcntl
import struct

class GetIPAddress:
    def __init__(self):
        return

    def getIP(self):
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            # print(hostname)
            return str(ip).strip()
        except Exception as e:
            return '127.0.0.1'
    
    def getlocalIP(self,device= 'wlan0'):
        try:
            #cmd = "hostname -I | cut -d\' \' -f1"
            #ip = str(subprocess.check_output(cmd, shell=True),'utf-8')
            ip = ni.ifaddresses(device)[ni.AF_INET][0]['addr']
            # print('local ip = ',ip)
            return ip
        except:
            return '127.0.0.1'
    
    def get_ip_address(self, interface):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ip = fcntl.ioctl(
                sock.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', interface[:15].encode('utf-8'))
            )[20:24]
            return socket.inet_ntoa(ip)
        except Exception:
            return None

    def get_local_ip(self):
        ip = self.get_ip_address('eth0')
        if ip:
            return ip
        ip = self.get_ip_address('wlan0')
        if ip:
            return ip
        return '172.0.0.1'
    

if __name__ == '__main__':
    a = GetIPAddress()
    # IP = a.getlocalIP('wlan0')
    IP = a.getIP()
    print(IP)
    #test passed