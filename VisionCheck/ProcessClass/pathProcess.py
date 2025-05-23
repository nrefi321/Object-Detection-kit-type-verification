import os
from datetime import date,datetime
import enum



def getdatetime1():
    today = date.today()
    return today.strftime("%b-%d-%Y")

def getdatetime():
    now = datetime.today()
    return now.strftime("%Y-%m-%d-%H-%M-%S-%MS")

class StatusLevel(enum.Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

class PathProcess:
    # mainPath = r'/home/vpd/Desktop/BG_test/BackGrinding_check'
    # mainPath = r'D:/fern/project_Fern/Backgrinding_jetson/BackGrinding_check'

    # configPath = '{}/config'.format(mainPath)
    # savePath = '{}/ImageSave'.format(mainPath)
    # logPath = '{}/log'.format(mainPath)
    # logfile = '{}/bot-VR20 {}.log'.format(logPath,getdatetime1())

    mainPath = r'D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check'
    
    configPath = '{}\config'.format(mainPath)
    savePath = '{}\ImageSave'.format(mainPath)
    logPath = '{}\log'.format(mainPath)
    logfile = '{}/bot-VR20 {}.log'.format(logPath,getdatetime1())
    
    def createdir(self):
        if not os.path.exists(PathProcess.mainPath):
            os.makedirs(PathProcess.mainPath)
        if not os.path.exists(PathProcess.savePath):
            os.makedirs(PathProcess.savePath)
        if not os.path.exists(PathProcess.logPath):
            os.makedirs(PathProcess.logPath)
        # if not os.path.exists(PathProcess.logfile):
        #     os.makedirs(PathProcess.logfile)
        if not os.path.exists(PathProcess.configPath):
            os.makedirs(PathProcess.configPath)

if __name__=='__main__':
    print(PathProcess.logfile)

    