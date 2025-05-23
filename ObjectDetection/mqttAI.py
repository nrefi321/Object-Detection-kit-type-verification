import time
import paho.mqtt.client as mqtt
import json
# from ProcessClass.pathProcess import StatusLevel
from getip import GetIPAddress
from repeatedTimer import RepeatedTimer
# from repeatedTimer import RepeatedTimer
# from getip import GetIPAddress

class MQTT:
    def __init__(self):
        # self.MQTTserver = 'pca571.nseb.co.th'
        self.MQTTserver = '10.151.27.1'
        # self.MQTTserver = '127.0.0.1'
        self.MQTTConnected = False
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.onConnectedMqtt
        self.mqtt_client.on_message = self.onMessageMqtt
        self.machineID = 'BGYolo-01'
        self.machineID_main = 'BG-01'
        # self.machineID_main = 'BG-test'
        self.callbackUpdateConfig = None
        self.callbackReqCurrentConfig = None
        self.callbackMqttstatus = None
        self.callbackSaveImgPath = None
        self.callbackReboot = None
        self.callbackResultYolo = None
        self.currentMachineIP = GetIPAddress().getlocalIP('wlan0')
        # self.currentMachineIP = GetIPAddress().get_local_ip()
        self.timer = RepeatedTimer(30,self.sendHeardbeat)
        self.useRobot = False

        print('init MQTT ')
    
    def topic(self):
        # #publish
        prefix = 'BackgrindingMQTT'
        pub_status = f'{prefix}/{self.machineID}/statusYolo'
        pub_result = f'{prefix}/{self.machineID_main}/resultYolo'
        pub_heartbeat = f'{prefix}/{self.machineID}/heartbeatYolo'
        pub_currentConfig = f'{prefix}/{self.machineID}/ret_currentconfigYolo'
        pub_savepath = f'{prefix}/{self.machineID}/savepathYolo'

        # #subscribe
        sub_updateconfig = f'{prefix}/{self.machineID}/updateconfigYolo'
        sub_currentconfig = f'{prefix}/{self.machineID}/req_currentconfigYolo'
        sub_savepath = f'{prefix}/{self.machineID}/savepath'
        sub_reboot = f'{prefix}/{self.machineID}/reboot'


        return [pub_status,pub_result,pub_heartbeat,pub_currentConfig,pub_savepath],\
            [sub_updateconfig,sub_currentconfig,sub_savepath,sub_reboot]

    def setMQTTServer(self,machineID,MQTTserver):
        if((MQTTserver != self.MQTTserver) or (machineID != self.machineID) or (self.MQTTConnected == False)):
            self.disconnectMQTT()
            self.MQTTserver = MQTTserver
            self.machineID = machineID
            print("New MQTT SERVER ID {}".format(self.MQTTserver))
            print("New MC ID {}".format(self.machineID))
            self.connectMqtt()
            # self.currentMachineIP = GetIPAddress().get_local_ip()
            self.currentMachineIP = GetIPAddress().getlocalIP('wlan0')
            while not self.MQTTConnected:
                print('wait Connecting')
                time.sleep(1)
        if(self.MQTTConnected and self.timer.is_running == False):
            time.sleep(5)
            self.timer.start()
    
    def connectMqtt(self):
        if(self.MQTTConnected):
            return
        try:
            # self.onlogMsg('MQTT Connecting',StatusLevel.INFO)
            self.onlogMsg('MQTT Connecting')
            port = 1883
            self.mqtt_client.connect(self.MQTTserver, port)
            self.mqtt_client.loop_start()
        except:
            # self.onlogMsg('MQTT Connection fail',StatusLevel.INFO)
            self.onlogMsg('MQTT Connection fail')
            self.MQTTConnected = False
            pass
    
    def disconnectMQTT(self):
        try:
            if(not self.timer.is_running and not self.MQTTConnected and not self.mqtt_client.is_connected):
                return
            self.MQTTConnected = False
            self.mqtt_client.disconnect()
            self.mqtt_client.loop_stop()
            self.timer.stop()
            time.sleep(5)
        except:
            pass

    # def onlogMsg(self,msg,statusLevel = StatusLevel.INFO):
    def onlogMsg(self,msg,statusLevel = "INFO"):
        if(self.callbackMqttstatus is not None):
            self.callbackMqttstatus(msg,statusLevel)
    
    def onResultYolo(self,res):
        if(self.callbackResultYolo is not None):
            self.callbackResultYolo(res)
    
    def onSaveImgPath(self,data):
        if(self.callbackSaveImgPath is not None):
            savepath = (data)
            self.callbackSaveImgPath(savepath)

    def onUpdateConfig(self,data):
        if(self.callbackUpdateConfig is not None):
            try:
                json_config = json.loads(data)
                self.callbackUpdateConfig(json_config)
            except:
                # self.onlogMsg('Config format not correct !!!',StatusLevel.ERROR)
                self.onlogMsg('Config format not correct !!!')

    def onReqcurrentconfig(self):
        if(self.callbackReqCurrentConfig is not None):
            currentconfig = self.callbackReqCurrentConfig()
            self.publish(json.dumps(currentconfig),3)
    
    def onReboot(self):
        if(self.callbackReboot is not None):
            self.callbackReboot()
            self.publish('reboot',0)    

    ################# Publish data to MQTT ##############

    def statusMsg(self,msg):
        self.publish(msg,0)
    
    def resultMsg(self,result):
        # self.publish(result,1)
        self.publish(json.dumps(result),1)

    def sendHeardbeat(self):
        try:
            param = {
                        "IP":self.currentMachineIP,
                        "machineId":self.machineID
            }
            self.publish(json.dumps(param),2)
            # print('heart beat')
        except:
            pass
    
    def sendSaveImgPath(self,msg):
        self.publish(msg,4)
    
    def publish(self,msg,i):
        if(self.MQTTConnected):
            topic,_ = self.topic()
            self.mqtt_client.publish(topic[i],msg)

    #################### MQTT Event ######################
    
    def onConnectedMqtt(self,client, userdata, flags, rc):
        self.MQTTConnected = True
        self.timer.start()
        print("On MQTT Connected Event.")
        _,topic = self.topic()
        print(topic[2])
        self.mqtt_client.subscribe(topic[0],qos=0)
        self.mqtt_client.subscribe(topic[1],qos=0)
        self.mqtt_client.subscribe(topic[2],qos=0)
        self.mqtt_client.subscribe(topic[3],qos=0)
        # self.onlogMsg('MQTT Connected',StatusLevel.INFO)
        self.onlogMsg('MQTT Connected')
        if rc==0:
            print("connected OK Returned code = ",rc)
        else:
            print("Bad connection Returned code = ",rc)

    def onMessageMqtt(self,client, userdata,msg):
        _,topic = self.topic()
        data = str(msg.payload.decode("utf-8"))
        print(f'data: {data}, topic: {msg.topic}')
        if(msg.topic == topic[0]):
            self.onUpdateConfig(data)
        elif(msg.topic == topic[1]):
            self.onReqcurrentconfig() #request current config
        elif(msg.topic == topic[2]):
            self.onSaveImgPath(data)
        elif(msg.topic == topic[3]):
            self.onReboot()

def testUpdateConfig(data):
    print('Test Case {}'.format(data))

def testCurrentConfig():
    return {
                "machineId" : "BGYolo-01",
                "scanRate" : 2,
                "monitor" : 1,
                "serverPath" : 'http://10.151.27.1/VR20ImageSave/api/VR20ImageSave',
                "MQTTServer" : '127.0.0.1',
                "useRobot" : False
            }
def testres():
    return [((1602, 789), (1677, 778), 'smallbox 0.65'), ((1165, 84), (1256, 73), 'smallhandle 0.74'), ((0, 530), (74, 519), 'whitebox 0.76')]

if __name__ == '__main__':
    mq = MQTT()
    mq.connectMqtt()
    mq.callbackReqCurrentConfig = testCurrentConfig
    mq.callbackUpdateConfig = testUpdateConfig
    
    # while True:
    #     mq.publish('test')
    #     time.sleep(1)
    # mq.publish('test',3)
    a = str(input())
    mq.disconnectMQTT()
    