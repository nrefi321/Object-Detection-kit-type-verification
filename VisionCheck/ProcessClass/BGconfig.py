# from multiprocessing.connection import wait
import os
import json
from turtle import width

from sqlalchemy import true
from ProcessClass.pathProcess import PathProcess
# from pathProcess import PathProcess
# from statusLevel import StatusLevel,PathProcess


class BackgrindConfig():
    def __init__(self):
        self.useAI = True
        self.hardwareConnect = False
        self.inputChannel = 0
        self.outputChannel = 0
        self.debouncetime = 0.5
        self.cameraAOI= {
            "width": 1920,
            "height": 1080
        }
        self.loadConfig()

    
    # def onlogMsg(self,msg,statusLevel = StatusLevel.INFO):
    #     if(self.updatelogStatus is not None):
    #         self.updatelogStatus(msg,statusLevel)

    def setnewConfig(self,newParam):
        try:
            useAI = bool(newParam['useAI'])
            hardwareConnect = bool(newParam['hardwareConnect'])
            inputChannel = int(newParam['inputChannel'])
            outputChannel = int(newParam['outputChannel'])
            debouncetime = float(newParam['debouncetime'])
            
            width = int(newParam['cameraAOI']['width'])
            height = int(newParam['cameraAOI']['height'])

            self.useAI = useAI
            self.hardwareConnect = hardwareConnect
            self.inputChannel = inputChannel
            self.outputChannel = outputChannel
            self.debouncetime = debouncetime
            self.cameraAOI = newParam['cameraAOI']

            print(newParam)
            self.saveconfig()
        except:
            # self.onlogMsg('Config format not correct !!!')
            print('Config format not correct !!!')
            pass
    
    def getCurrentConfig(self):
        return  {
                    "useAI" : self.useAI,
                    "hardwareConnect" : self.hardwareConnect,
                    "inputChannel" : self.inputChannel,
                    "outputChannel" : self.outputChannel,
                    "debouncetime" : self.debouncetime,
                    "cameraAOI" : self.cameraAOI 
                }

    def createdir(self):
        config_dir = self.pathConfig()
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

    def pathConfig(self):
        return PathProcess.configPath
    
    def loadConfig(self):
        try:
            config_dir = os.path.join(self.pathConfig(),'config.json')
            self.createdir()
            param = {
                        "useAI" : self.useAI,
                        "hardwareConnect" : self.hardwareConnect,
                        "inputChannel" : self.inputChannel,
                        "outputChannel" : self.outputChannel,
                        "debouncetime" : self.debouncetime,
                        "cameraAOI" : self.cameraAOI 
                    }
            if not os.path.exists(config_dir):
                json_data = json.dumps(param, indent=2)
                f = open(config_dir, 'x')
                f.write(json_data)
                f.close()
            with open(config_dir) as file:
                param = json.load(file)
                self.useAI = bool(param['useAI'])
                self.hardwareConnect = bool(param['hardwareConnect'])
                self.inputChannel = int(param['inputChannel'])
                self.outputChannel = int(param['outputChannel'])
                self.debouncetime = float(param['debouncetime'])
                self.cameraAOI = (param['cameraAOI'])
        except:
            self.saveconfig()
        return param

    def saveconfig(self):
        config_dir = os.path.join(self.pathConfig(),'config.json')
        self.createdir()
        param = {
            "useAI" : self.useAI,
            "hardwareConnect" : self.hardwareConnect,
            "inputChannel" : self.inputChannel,
            "outputChannel" : self.outputChannel,
            "debouncetime" : self.debouncetime,
            "cameraAOI" : self.cameraAOI 
        }
        json_data = json.dumps(param, indent=2)
        f = open(config_dir, 'w')
        f.write(json_data)
        f.close()

if __name__ == '__main__':
    BG = BackgrindConfig()
    # param = {"useAI": true, "hardwareConnect": true, "inputChannel": 3, "debouncetime": 0.6, "cameraAOI": {"width": 2592, "height": 1944}}
    # param = {"useAI": true, "hardwareConnect": true, "inputChannel": 3, "debouncetime": 0.6, "cameraAOI": {"width": 1920, "height": 1080}}
    param = {"useAI": true, "hardwareConnect": true, "inputChannel": 0, "outputChannel": 0, "debouncetime": 0.6, "cameraAOI": {"width": 2048, "height": 1536}}
    BG.setnewConfig(param)
    # BG.loadConfig()
    # vr20.saveconfig()
    print(BG.getCurrentConfig())
    # imgrawDelay = vr20.paramBotProcess['imgRawDelay']
    # clickDelay = vr20.paramBotProcess['imgRawDelay']
    # print(BG.cameraAOI['width'])
    
    
    #Test Pass