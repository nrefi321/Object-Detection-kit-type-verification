import time
import paho.mqtt.client as mqtt
import json
from ProcessClass.pathProcess import StatusLevel
from ProcessClass.getip import GetIPAddress
from ProcessClass.repeatedTimer import RepeatedTimer

import cv2 as cv
# from repeatedTimer import RepeatedTimer
# from getip import GetIPAddress
# from pathProcess import StatusLevel

class MQTT:
    def __init__(self):
        self.MQTTserver = 'pca571.nseb.co.th'
        # self.MQTTserver = '10.151.27.1'
        # self.MQTTserver = '127.0.0.1'
        self.MQTTConnected = False
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.onConnectedMqtt
        self.mqtt_client.on_message = self.onMessageMqtt
        # self.machineID = 'BG-01'
        self.machineID = 'BG-test'
        self.machineID_sub = 'BGYolo-01'
        self.callbackUpdateConfig = None
        self.callbackReqCurrentConfig = None
        self.callbackMqttstatus = None
        self.callbackMqttresult = None
        self.callbackMqttstate = None
        self.callbackMqttb64Img = None
        self.callbackSaveImgPath = None
        self.callbackReboot = None
        self.callbackResultYolo  = None
        self.callbackTestcapture = None
        self.currentMachineIP = GetIPAddress().get_local_ip()
        self.timer = RepeatedTimer(30,self.sendHeardbeat)
        self.useRobot = False

        # print('init MQTT ')
    
    def topic(self):
        prefix = 'BackgrindingMQTT'

        # Publish topics
        pub_status = f'{prefix}/{self.machineID}/status'
        pub_heartbeat = f'{prefix}/{self.machineID}/heartbeat'
        pub_result = f'{prefix}/{self.machineID}/result'
        pub_currentConfig = f'{prefix}/{self.machineID}/ret_currentconfig'
        pub_savepath = f'{prefix}/{self.machineID_sub}/savepath'
        pub_reboot = f'{prefix}/{self.machineID_sub}/reboot'
        pub_state = f'{prefix}/{self.machineID}/state'
        pub_b64img = f'{prefix}/{self.machineID}/b64img'

        # Subscribe topics
        sub_updateconfig = f'{prefix}/{self.machineID}/updateconfig'
        sub_currentconfig = f'{prefix}/{self.machineID}/req_currentconfig'
        sub_reboot = f'{prefix}/{self.machineID}/reboot'
        sub_result = f'{prefix}/{self.machineID}/resultYolo'
        sub_testcaprute = f'{prefix}/{self.machineID}/testcapture'

        return [pub_status, pub_result, pub_heartbeat, pub_currentConfig, pub_savepath, pub_reboot, pub_state, pub_b64img], \
            [sub_updateconfig, sub_currentconfig, sub_reboot, sub_result, sub_testcaprute]

    def setMQTTServer(self,machineID,MQTTserver):
        if((MQTTserver != self.MQTTserver) or (machineID != self.machineID) or (self.MQTTConnected == False)):
            self.disconnectMQTT()
            self.MQTTserver = MQTTserver
            self.machineID = machineID
            print("New MQTT SERVER ID {}".format(self.MQTTserver))
            print("New MC ID {}".format(self.machineID))
            self.connectMqtt()
            self.currentMachineIP = GetIPAddress().get_local_ip()
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
            self.onlogMsg('MQTT Connecting',StatusLevel.INFO)
            # self.onlogMsg('MQTT Connecting')
            port = 1883
            self.mqtt_client.connect(self.MQTTserver, port)
            self.mqtt_client.loop_start()
        except:
            self.onlogMsg('MQTT Connection fail',StatusLevel.INFO)
            # self.onlogMsg('MQTT Connection fail')
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

    def onlogMsg(self,msg,statusLevel = StatusLevel.INFO):
    # def onlogMsg(self,msg,statusLevel = ""):
        if(self.callbackMqttstatus is not None):
            self.callbackMqttstatus(msg,statusLevel)
    
    def onResult(self,msg,statusLevel = StatusLevel.INFO):
    # def onlogMsg(self,msg,statusLevel = ""):
        if(self.callbackMqttresult is not None):
            self.callbackMqttresult(msg,statusLevel)
    
    def onState(self,msg,statusLevel = StatusLevel.INFO):
    # def onlogMsg(self,msg,statusLevel = ""):
        if(self.callbackMqttstate is not None):
            self.callbackMqttstate (msg,statusLevel)
    
    def onB64Img(self,msg,statusLevel = StatusLevel.INFO):
    # def onlogMsg(self,msg,statusLevel = ""):
        if(self.callbackMqttb64Img is not None):
            self.callbackMqttb64Img(msg,statusLevel)
    
    def onResultYolo(self,res):
        if(self.callbackResultYolo is not None):
            # self.callbackResultYolo(res)
            try:
                json_res = json.loads(res)
                self.callbackResultYolo(json_res)
            except:
                self.onlogMsg('Result format not correct !!!',StatusLevel.ERROR)
    
    def onTestcapture(self):
        if(self.callbackTestcapture is not None):
            self.callbackTestcapture()
    
    def onSaveImgPath(self,msg):
        if(self.callbackSaveImgPath is not None):
            self.callbackSaveImgPath(msg)

    def onUpdateConfig(self,data):
        if(self.callbackUpdateConfig is not None):
            try:
                json_config = json.loads(data)
                self.callbackUpdateConfig(json_config)
            except:
                self.onlogMsg('Config format not correct !!!',StatusLevel.ERROR)
                # self.onlogMsg('Config format not correct !!!')

    def onReqcurrentconfig(self):
        if(self.callbackReqCurrentConfig is not None):
            currentconfig = self.callbackReqCurrentConfig()
            self.publish(json.dumps(currentconfig),3)
    
    def onReboot(self):
        if(self.callbackReboot is not None):
            self.callbackReboot()
            self.publish('reboot',5)  
    

    ################# Publish data to MQTT ##############

    def statusMsg(self,msg):
        self.publish(msg,0)
    
    def resultMsg(self,result_json):
        self.publish(json.dumps(result_json),1)

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

    def stateMsg(self,msg):
        self.publish(msg,6)
    
    def b64Img(self,msg):
        self.publish(msg,7)
    
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
        print(topic)
        self.mqtt_client.subscribe(topic[0],qos=0)
        self.mqtt_client.subscribe(topic[1],qos=0)
        self.mqtt_client.subscribe(topic[2],qos=0)
        self.mqtt_client.subscribe(topic[3],qos=0)
        self.mqtt_client.subscribe(topic[4],qos=0)
        self.onlogMsg('MQTT Connected',StatusLevel.INFO)
        # self.onlogMsg('MQTT Connected')

    def onMessageMqtt(self,client, userdata,msg):
        _,topic = self.topic()
        data = str(msg.payload.decode("utf-8"))
        print(data,msg.topic)
        if(msg.topic == topic[0]):
            self.onUpdateConfig(data)
        elif(msg.topic == topic[1]):
            self.onReqcurrentconfig() #request current config
        elif(msg.topic == topic[2]):
            self.onReboot()
        elif(msg.topic == topic[3]):
            self.onResultYolo(data)
        elif(msg.topic == topic[4]):
            self.onTestcapture()
        

def testUpdateConfig(data):
    print('Test Case {}'.format(data))

def testCurrentConfig():
    return {
                "machineId" : "BG-01",
                "scanRate" : 2,
                "monitor" : 1,
                "serverPath" : 'http://10.151.27.1/VR20ImageSave/api/VR20ImageSave',
                "MQTTServer" : '127.0.0.1',
                "useRobot" : False
            }
def testcapture():
    print('Capture test mqtt')
    grey_img = cv.imread(r'D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\ImageSave\2022-12-07-17-37-46-37S.jpg', cv.IMREAD_GRAYSCALE)
    status = cv.imwrite(r'D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\ImageSave\test.png',grey_img)
    print("Image written to file-system : ",status)

if __name__ == '__main__':
    mq = MQTT()
    mq.connectMqtt()
    # mq.callbackReqCurrentConfig = testCurrentConfig
    # mq.callbackUpdateConfig = testUpdateConfig
    mq.callbackTestcapture = testcapture
    # while True:
    #     mq.publish('test')
    #     time.sleep(1)
    # mq.publish('test',3)
    a = str(input())
    mq.disconnectMQTT()
    