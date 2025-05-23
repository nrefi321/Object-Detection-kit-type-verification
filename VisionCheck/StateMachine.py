import os
import cv2 as cv
import time
import base64
import random
import datetime
import numpy as np
from pyueye import ueye
from ProcessClass.ueyeCamera import UeyeCamera
from ProcessClass.GPIO import JetsonGPIO
from ProcessClass.pathProcess import PathProcess, getdatetime, StatusLevel
from ProcessClass.MQTTControl import MQTT
from ProcessClass.BGconfig import BackgrindConfig
from ProcessClass.logicAnalysis import Analysis

class StateMachine:
    def __init__(self):
        self.path = PathProcess()
        self.pathsaveImg = self.path.savePath
        self.config = BackgrindConfig()
        self.analysis = Analysis()
        self.camera = UeyeCamera()
        self.gpio = JetsonGPIO()
        self.MQ = MQTT()

        self.state = 's1'
        self.io = 0
        self.current_io = 0
        self.count = 0  
        self.CallbackClearstate = None
        self.resultYolo = None
        self.procReboot = False
        self.useAI = False
        self.hardwareConnect = True

        self._setup_mqtt()
        self.reloadconfig()

    def _setup_mqtt(self):
        self.MQ.connectMqtt()
        self.MQ.callbackUpdateConfig = self.onMQUpdateConfig
        self.MQ.callbackReqCurrentConfig = self.onCallCurrentConfig
        self.MQ.callbackMqttstatus = self.statusUpdate
        self.MQ.callbackSaveImgPath = self.sendImgPath
        self.MQ.callbackReboot = self.onReboot
        self.MQ.callbackResultYolo = self.onResultYolo
        self.MQ.callbackTestcapture = self.onTestcapture

    def reloadconfig(self):
        try:
            self.config.loadConfig()
            self.useAI = self.config.useAI
            self.hardwareConnect = self.config.hardwareConnect
            self.inputChannel = self.config.inputChannel
            self.outputChannel = self.config.outputChannel
            self.debouncetime = self.config.debouncetime
            self.cameraAOI = self.config.cameraAOI
            self.width = self.cameraAOI['width']
            self.height = self.cameraAOI['height']
            self.MQ.setMQTTServer('BG-01', '10.151.27.1')
            return True
        except Exception as e:
            print(f"Error in reloadconfig: {e}")
            return False

    def run(self):
        self.procReboot = False
        self.count = 0
        reConnect = 0
        camconnect = self.camera.connection(self.width, self.height)
        print(f'connection {camconnect}')
        try:
            while(camconnect == False):
                try:
                    if (self.procReboot == True):
                        print('break')
                        break  
                    if(reConnect <= 10):
                        print(f'count reConnect {reConnect}')
                        camconnect = self.camera.connection(self.width,self.height)
                        if(camconnect):
                            print(camconnect)
                            reConnect = 0
                        else:
                            reConnect+=1
                        time.sleep(2)
                    else:
                        print("Can not connect Camera")
                        break
                except:
                    break

            if (camconnect):    
                self.statusUpdate('Camera Connected')
                res = None
                i = 0
                print('Start')
                self.read_io()
                while self.camera.nRet == ueye.IS_SUCCESS:
                    # Skip unused buffer frames
                    for _ in range(self.camera.bufferCount):
                        array = ueye.get_data(
                            self.camera.pcImageMemory,
                            self.camera.width,
                            self.camera.height,
                            self.camera.nBitsPerPixel,
                            self.camera.pitch,
                            copy=False
                        )

                    frame = np.reshape(array, (self.camera.height.value, self.camera.width.value, self.camera.bytes_per_pixel))
                    frame = cv.cvtColor(frame, cv.COLOR_BGRA2BGR)
                    frame_resized = cv.resize(frame, (0, 0), fx=0.3, fy=0.3)
                    self.MQ.statusMsg(f'State {self.state}')

                    if self.procReboot:
                        print("Reboot triggered, breaking loop.")
                        break

                    # FSM states
                    if self.state == 's1':
                        self.handle_state_s1()
                    elif self.state == 's2':
                        self.handle_state_s2(frame)
                    elif self.state == 's3':
                        self.handle_state_s3(frame)
                    elif self.state == 's4':
                        self.handle_state_s4()
                        del array
                    elif self.state == 's5':
                        self.handle_state_s5()
                        del array
                    
                    key = cv.waitKey(1)
                    if key == ord('q'):
                        break
                    elif key == ord('a'):
                        self.CallbackClearstate = True

                    if (self.procReboot == True):
                        print('break from reboot')
                        break
        finally:
            self.DisconnectAll()

    # --- FSM Handlers ---
    def handle_state_s1(self):
        self.sendState('s1')
        self.MQ.statusMsg('Checking door...')
        self.read_io()
        # If door is closed, wait until it's open
        if self.current_io == 1:
            self.close_door()
            while self.current_io == 1:
                self.read_io()
                time.sleep(0.1)
            self.open_door()
        else:
            self.open_door()
        self.state = 's2'

    def handle_state_s2(self, frame):
        self.sendState('s2')
        self.MQ.statusMsg('Waiting for door to close...')
        while self.current_io == 0:
            self.read_io()
        self.SaveImg(frame)
        self.state = 's3'

    def handle_state_s3(self, frame):
        self.sendState('s3')
        self.MQ.statusMsg('Waiting for AI-Yolo...')
        self.resultYolo = None
        timeout = 5
        poll_interval = 0.5
        waited = 0

        while self.resultYolo is None and waited < timeout:
            time.sleep(poll_interval)
            waited += poll_interval

        # self.resultYolo = [[[1140, 392], [1857, 1080], "black_6 0.91"], [[860, 3], [1066, 351], "handle_small 0.93"], [[14, 320], [916, 1079], "nobox 0.96"]]  # Simulated result

        if self.resultYolo is not None:
            res = self.LogicAnalysis(self.resultYolo)
            if res:
                self.statusUpdate(f'Setup OK: {res}')
                self.state = 's1'
            else:
                self.statusUpdate(f'Setup NG: {res}', StatusLevel.WARNING)
                self.state = 's4'
        else:
            self.statusUpdate('No YOLO result received')
            res = None
            self.state = 's4'

        self.Addtext(frame, res)
        self.sendResult(res)

    def handle_state_s4(self):
        self.sendState('s4')
        while self.count == 0:
            self.MQ.statusMsg('Warning Alarm')
            self.warning_alarm()
            self.count += 1
        self.read_io()
        while self.current_io == 1:
            # self.MQ.statusMsg(f'Warning in loop {self.current_io}')
            self.checkClearState()
            self.read_io()
          
        if self.current_io == 0:
            self.state = 's1'
            self.statusUpdate('State cleared, ready for setup')

    def handle_state_s5(self):
        self.sendState('s5')
        self.clear_state()
        self.CallbackClearstate = None
        self.count = 0
        self.state = 's1'

    # --- Helper Methods (unchanged or slightly updated) ---
    def clear_state(self):
        self.gpio.outputWrite(self.outputChannel, on=False)
        self.statusUpdate('Clear state')

    def checkClearState(self):
        if self.getCallbackClearstate():
            self.state = 's5'
        else:
            self.CallbackClearstate = True
            self.state = 's5'
            self.MQ.statusMsg('Auto clear state')

    def getCallbackClearstate(self):
        if self.CallbackClearstate is not None:
            return True
        else:
            return False
        
    def check_door(self):
        if self.io == 1:
            print('Door is closed')
        else:
            print('Door is open')

    def close_door(self):
        # print('Closing door')
        self.MQ.statusMsg('Closing door')

    def open_door(self):
        # print('Door is opening ... waiting for setup ...')
        self.MQ.statusMsg('Door is opening ... waiting for setup ...')

    def capture_image(self):
        print('Capturing image')
        self.result_from_yolo = 'some result'

    def TestProcCapture(self):
        array = ueye.get_data(self.camera.pcImageMemory, self.camera.width, self.camera.height, self.camera.nBitsPerPixel, self.camera.pitch, copy=False)
        frame = np.reshape(array,(self.camera.height.value, self.camera.width.value, self.camera.bytes_per_pixel))
        frame = cv.cvtColor(frame,cv.COLOR_BGRA2BGR,frame,3)
        filename = '{}/{}.jpg'.format(self.pathsaveImg,getdatetime())
        cv.imwrite(filename,frame)
        self.sendImgPath(filename)

    def SaveImg(self, frame):
        filename = os.path.join(self.pathsaveImg, f"{getdatetime()}.jpg")
        cv.imwrite(filename, frame)
        self.sendImgPath(filename)

    def Addtext(self, frame, res):
        # resultTestPath = r'D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\ImageResult'
        resultTestPath = r'/home/vpd/Desktop/BG/BackGrinding_check/ImageResult'
        font = cv.FONT_HERSHEY_SIMPLEX
        org = (20,80)
        fontscale = 3
        thickness = 5
        if res:
            color = (0,255,0)
            frame = cv.putText(frame,f' OK ', org, font, 
                    fontscale, color, thickness, cv.LINE_AA)
        elif res == False:
            color = (0,0,255)
            frame = cv.putText(frame,f' NG ', org, font, 
                    fontscale, color, thickness, cv.LINE_AA)
        else:
            color = (255,0,0)
            frame = cv.putText(frame,f' None ', org, font, 
                    fontscale, color, thickness, cv.LINE_AA)
            
        img = '{}/{}.jpg'.format(resultTestPath,getdatetime())
        cv.imwrite(img,frame)
        self.sendB64Image(frame)

    def LogicAnalysis(self, res):
        if len(res) != 3:
            return False
        return self.analysis.logicAnalysis(res)

    def warning_alarm(self):
        self.gpio.outputWrite(self.outputChannel,on=True)
        self.statusUpdate('Warning alarm',statusLevel=StatusLevel.WARNING)
        pass

    def read_io(self):
        io = self.gpio.readInputDebounce(self.inputChannel, self.debouncetime)

        # simulated_io = random.choice([True, False])
        # io = 1 if simulated_io else 0

        self.sendResult(io)
        self.set_io(io)
        time.sleep(0.2)

    def set_io(self, value):
        self.io = value
        self.current_io = value

    def image2base64(self,image):
        _, buffer = cv.imencode('.jpg', image)
        base64_string = base64.b64encode(buffer).decode()

        return base64_string

    def statusUpdate(self, msg, statusLevel=StatusLevel.INFO):
        try:
            level = statusLevel.name
            status = f"{datetime.datetime.now()} {level} {msg}"
            filename = PathProcess.logfile
            with open(filename, 'a' if os.path.exists(filename) else 'w') as log:
                log.write(status + '\n')
            print(status)
            self.MQ.statusMsg(status)
        except Exception:
            pass

    def DisconnectAll(self):
        self.gpio.closeIO()
        self.camera.disconnect()
        self.MQ.disconnectMQTT()
        cv.destroyAllWindows()

    # --- MQTT Callbacks ---
    def onMQUpdateConfig(self, data):
        self.config.setnewConfig(data)
        self.reloadconfig()

    def onCallCurrentConfig(self):
        return self.config.getCurrentConfig()

    def onReboot(self):
        self.statusUpdate('On reboot before publish')
        self.procReboot = True

    def onResultYolo(self, data):
        self.resultYolo = data if data else None

    def onTestcapture(self):
        self.TestProcCapture()

    # --- MQTT Communication ---
    def sendResult(self, msg):
        self.MQ.resultMsg(msg)

    def sendState(self, msg):
        self.MQ.stateMsg(msg)

    def sendB64Image(self, frame):
        img = cv.resize(frame, (0, 0), fx=0.3, fy=0.3)
        b64 = self.image2base64(img)
        self.MQ.b64Img(b64)

    def sendImgPath(self, msg):
        try:
            filename = PathProcess.logfile
            if os.path.exists(filename):
                append_write = 'a'  # append if exists
            else:
                append_write = 'w'  # create new file
            with open(filename, append_write) as log:
                log.write(msg + '\n')
            self.MQ.sendSaveImgPath(msg)
        except:
            pass

    def mqttDisconnect(self):
        self.MQ.disconnectMQTT()

if __name__ == '__main__':
    sm = StateMachine()
    try:
        sm.run()
    except KeyboardInterrupt:
        sm.DisconnectAll()
    except Exception as e:
        print(f"An error occurred: {e}")
        sm.DisconnectAll()
    finally:
        sm.DisconnectAll()
        print("State machine stopped.")
