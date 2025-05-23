from detection_clean import Detector
from mqttAI import MQTT
import time
import datetime
import os
import subprocess


class AIProcess:
    def __init__(self, use_mqtt=True):
        self.imgPath = None      
        self.use_mqtt = use_mqtt
        self.detection = None
        self.procReboot = False

        if self.use_mqtt:
            self.MQ = MQTT()
            self.MQ.connectMqtt()
            self.MQ.callbackSaveImgPath = self.onSaveImgPath
            self.MQ.callbackReboot = self.onReboot
            self.MQ.callbackResultYolo = self.onSendResult
               
    def onSendResult(self, data):
        if self.use_mqtt:
            self.MQ.resultMsg(data)

    def onSaveImgPath(self, data):       
        path = r'D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\ImageSave'
        try:
            for filename in os.listdir(path):
                full_path = os.path.join(path, filename)
                if full_path == data:
                    self.imgPath = full_path
                    print(f'Found file: {full_path}')
        except Exception as e:
            print(f'Error reading directory: {e}')
    
    def onReboot(self):
        print('Reboot command received.')
        self.procReboot = True
    
    def statusUpdate(self, msg):
        try:
            status = f"{datetime.datetime.now()} {msg}"
            print(status)
            if self.use_mqtt:
                self.MQ.statusMsg(status)
        except Exception as e:
            print(f"Status update failed: {e}")
        
    def disconnectMQTT(self):
        if self.use_mqtt:
            self.MQ.disconnectMQTT()
    
    def aiProc(self):
        self.MQ.connectMqtt()
        self.MQ.setMQTTServer('BGYolo-01', '10.151.27.1')

        self.statusUpdate("AI Connected .. Waiting for LOAD MODEL")
        self.detection = Detector(weights_path=r'D:\fern2022\Backgrinding\dev_test\yolov7\BG01.pt')
        self.statusUpdate("AI Ready ..")

        # 👉 Launch main.py in parallel
        # subprocess.Popen(['python', 'main.py'])

        try:
            while True:
                if self.imgPath:
                    if os.path.exists(self.imgPath):
                        print('Processing image...')
                        result = self.detection.detect(
                            source_path=self.imgPath,
                            save_dir=r'D:\fern2022\Backgrinding\dev_test\yolov7\DetectionImage'
                        )
                        print(f'Result: {result}')
                        self.onSendResult(result)
                    else:
                        print("Image path does not exist.")
                        self.onSendResult([])

                    self.imgPath = None  # Reset image path after processing
                else:
                    time.sleep(0.1)

                if self.procReboot:
                    self.statusUpdate("Reboot requested.")
                    break

        except Exception as e:
            print(f"Exception in AI processing loop: {e}")
            self.onSendResult([])


if __name__ == '__main__':
    ai = AIProcess()
    try:
        ai.aiProc()
    except Exception as e:
        print(f"Fatal error: {e}")
        ai.disconnectMQTT()
        print("Process ended.")
