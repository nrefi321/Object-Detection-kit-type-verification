import socket
import netifaces as ni

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
            #print('local ip = ',ip)
            return ip
        except:
            return '127.0.0.1'

if __name__ == '__main__':
    a = GetIPAddress()
    IP = a.getlocalIP('wlan0')
    print(IP)
    #test passed
