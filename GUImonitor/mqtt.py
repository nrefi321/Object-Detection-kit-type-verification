import paho.mqtt.client as mqtt
import time
import json

class MQTTSubscriber:
    def __init__(self):
        broker_ip = "10.151.27.1"
        # broker_ip = 'pca571.nseb.co.th'
        broker_port = 1883

        self.client = mqtt.Client()

        self.broker_ip = broker_ip
        self.broker_port = broker_port
        self.machineID = "BG-01"
        # self.machineID = 'BG-test'

        self.callbackMqttState = None 
        self.callbackMqttResult = None 
        self.callbackMqttb64Img = None
    
    def onResult(self,msg):
    # def onlogMsg(self,msg,statusLevel = ""):
        if(self.callbackMqttResult is not None):
            try:
                json_res = json.loads(msg)
                self.callbackMqttResult(json_res)
            except:
                pass
    
    def onState(self,msg):
    # def onlogMsg(self,msg,statusLevel = ""):
        if(self.callbackMqttState is not None):
            self.callbackMqttState(msg)
    
    def onB64Img(self,msg):
    # def onlogMsg(self,msg,statusLevel = ""):
        if(self.callbackMqttb64Img is not None):
            try:
                # json_res = json.loads(msg)
                self.callbackMqttb64Img(msg)
            except:
                pass
    def on_message(self, client, userdata, msg):
        topic = self.topic()
        data = str(msg.payload.decode("utf-8"))
        # print(data,msg.topic)
        if(msg.topic == topic[0]):
            print(topic[0],data)
            self.onState(data)
            # self.onReboot()
        elif(msg.topic == topic[1]):
            print(topic[1],data)
            self.onResult(data)
            # self.onResultYolo(data)
        elif(msg.topic == topic[2]):
            print(topic[2])
            self.onB64Img(data)

    def connect(self):

        self.client.on_message = self.on_message
        self.client.connect(self.broker_ip, self.broker_port)

    def subscribe(self):
        self.client.loop_start()
        self.topics = self.topic()
        for topic in self.topics:
            self.client.subscribe(topic)
    
    def topic(self):

        prefix = 'BackgrindingMQTT'

        sub_state = '{}/{}/state'.format(prefix,self.machineID)
        sub_result = '{}/{}/result'.format(prefix,self.machineID)
        sub_b64img = '{}/{}/b64img'.format(prefix,self.machineID)
        return [sub_state,sub_result,sub_b64img]

    def run(self):
        self.connect()
        self.subscribe()
        # while True:
        #     pass

if __name__=='__main__':
    subscriber = MQTTSubscriber()
    subscriber.run()
