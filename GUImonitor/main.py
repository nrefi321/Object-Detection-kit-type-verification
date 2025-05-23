import threading
import time
import random
from gui02 import Guimonitor
from mqtt import MQTTSubscriber
import base64 
import numpy as np 
import cv2
from PIL import Image


class Proc:
    def __init__(self,gui):
        self.gui = gui
        self.numberList = [1, 4, 5, 2, 7, 8, 9, 10]
        self.running = False
        self.clickReset = False
        self.clickStop = False
        self.clickDone = False
        self.subscriber = MQTTSubscriber()  # Create an instance of MQTTSubscriber
        # self.subscriber.run()
        self.imgPil = None
        self.state = None 
        self.result = None
        self.b64Img = None
        self.subscriber.callbackMqttState = self.onMqttState
        self.subscriber.callbackMqttResult = self.onMqttResult
        self.subscriber.callbackMqttb64Img = self.onMqttb64Img

    def onMqttState(self,data):   
        if data is not None: 
            self.state = data
        else:
            self.state = None 
        # print(self.state)
        # self.gui.stateStatus(self.state)
    
    def onMqttResult(self,data):   
        if data is not None: 
            self.result = data
            # print(f'onResult : {self.result} {type(self.result)}')
        else:
            self.result = None 
    
    def onMqttb64Img(self,data):   
        if data is not None: 
            # b64Img = data
            self.imagefrom64 = self.base64toimage(data)
            img_bgr = cv2.cvtColor(self.imagefrom64, cv2.COLOR_BGR2RGB)
            # PIL_image = Image.fromarray(np.uint8(img_bgr)).convert('RGB')
            PIL_image = Image.fromarray(np.uint8(img_bgr))
            # print(f'img decode >>>>>>>>>> {type(PIL_image)}')
            self.imgPil = PIL_image
            # cv2.imwrite(r'D:\fern\project_Fern\Backgrinding_jetson\BG-ui\img64_1.jpg',self.imagefrom64)
            # cv2.waitKey(0)
        else:
            self.b64Img = None 
    
    def onReset(self):
        print("Reset button clicked")
        self.clickReset = True
        print(f'in onReset {self.clickReset}')
    
    def onStop(self):
        self.clickStop = True
        print(f'in onStop {self.clickStop}')
    
    def ondoneEdit(self):
        print("Done Editting")
        self.clickDone = True
    
    def base64toimage(self,base64_string):
        image_bytes = base64.b64decode(base64_string)
        np_arr = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return image

    def testProc(self):
        random_num = random.choice(self.numberList)
        ran = random_num % 3
        if ran == 2:
            res = True
        elif ran == 1:
            res = False
        else:
            res = False
        return res

    def testfileimg(self):
        filename = r"D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\resourceimage\imgfree.jpg"
        img = cv2.imread(filename)
        image = Image.fromarray(np.uint8(img)).convert('RGB')
        return image
    
    def run(self):
        self.running = True
        self.subscriber.run()
        while self.running:
            # filename = r"D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\resourceimage\imgfree.jpg"
            # filename = self.testfileimg()
            # self.gui.guiImagePath(filename)

            self.gui.guiImagePath(self.imgPil)

            # if self.imgPil is not None:
            #     self.gui.guiImagePath(self.imgPil)


            # res = self.testProc()
            res = self.result
            state = self.state
            self.gui.stateStatus(state)
            print(f'state ---- {state}')
            # print(res)
            self.gui.check_data(res)
            if res != True:
                # self.gui.guiImagePath(filename)
                self.gui.guiImagePath(self.imgPil)
            if self.clickReset:
                print('reset')
                print('reset')
                print('reset')
                time.sleep(1)
                self.clickReset = False
            else:
                # print('no reset')
                statenow = 'no reset'
            if self.clickDone:
                print('reloadconfig')
                self.clickDone = False
            if self.clickStop:
                self.stop()
            time.sleep(2)
    
    def stop(self):
        self.running = False
    
    def setCallback(self):
        self.gui.set_reset_callback(self.onReset)  # Set the callback function
        self.gui.set_stop_callback(self.onStop)  # Set the callback function
        self.gui.set_doneEdit_callback(self.ondoneEdit)  # Set the callback function

if __name__ == '__main__':
    # gui = App()
    gui = Guimonitor()
    proc = Proc(gui)
    try:
        proc.setCallback()
        t = threading.Thread(target=proc.run)
        t.start()
        gui.start()
        # gui.mainloop()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Stopping thread and cleaning up.")
        proc.stop()
        t.join(timeout=5)
        print("Exited cleanly.")

    # gui = App()

    # # gui = Guimonitor()
    # proc = Proc(gui)
    # gui.set_reset_callback(proc.onReset)  # Set the callback function
    # t = threading.Thread(target=proc.run)
    # t.start()
    # # gui.start()
    # gui.mainloop()



    # pyueye 4.90