import cv2 as cv
from ProcessClass.getChecklistData import ChecklistData
# from ProcessClass.gui import ColorChanger
# from getChecklistData import ChecklistData
# from gui import ColorChanger
import tkinter as tk

class Analysis:
    def __init__(self):
        self.checklist = ChecklistData()
        # self.root = tk.TK()
        # self.colorchange = ColorChanger(tk.Tk())
        self.pos = []

    def calculateIntersection(self,a0, a1, b0, b1):
        if a0 >= b0 and a1 <= b1:  # Contained
            intersection = a1 - a0
        elif a0 < b0 and a1 > b1:  # Contains
            intersection = b1 - b0
        elif a0 < b0 and a1 > b0:  # Intersects right
            intersection = a1 - b0
        elif a1 > b1 and a0 < b1:  # Intersects left
            intersection = b1 - a0
        else:
            intersection = 0
        return intersection
    
    def findIntersectArea(self,res):
        p0,p1= res
        x0,y0 = p0
        x1,y1 = p1 
        # top = [485, 7, 2095,865]
        # left = [1,280,1240,1944]
        # right = [1375,280,2590,1944]
        top = [350, 0, 1562,602]
        left = [1,314,853,1006]
        right = [992,314,1916,1007]

        aoi = [top,left,right]
        
        position = ""
        for i in range(len(aoi)):
            X0, Y0, X1, Y1 = aoi[i]
            AREA = float((x1 - x0) * (y1 - y0))
            width = self.calculateIntersection(x0, x1, X0, X1)
            height = self.calculateIntersection(y0, y1, Y0, Y1)
            area = width * height
            # print(area)
            # print(AREA)
            percent = area / AREA
            # print(f'{i} {percent} % ')
            if (percent >= 0.65):
                if i == 0 :
                    position = "top"
                elif i == 1:
                    position = "left"
                elif i == 2:
                    position = "right"
                else:
                    print('not in area')
                # print(f'{position} IsOverlap')
                self.pos.append(position)
        return self.pos


    def findOverlap(self,x0, y0, x1, y1):
        X0, Y0, X1, Y1, = [485, 7, 2095,865]
        # AREA = float((X1 - X0) * (Y1 - Y0))
        AREA = float((X1 - X0) * (Y1 - Y0))
        print(AREA)
        width = self.calculateIntersection(x0, x1, X0, X1)
        height = self.calculateIntersection(y0, y1, Y0, Y1)
        area = width * height
        print(area)
        print(width,height)
        percent = area / AREA
        # percent = AREA / area
        print(f' {percent} % ')
        if (percent >= 0.65):
            print('IsOverlap')
            return True
        else:
            return False

    def rearrangeList(self,position,label):
        order = [(position.index('top')),(position.index('left')),(position.index('right'))]
        position = [position[i] for i in order]
        label = [label[i] for i in order]
        label = [((label[0]).split(' ',1)[0]),((label[1]).split(' ',1)[0]),((label[2]).split(' ',1)[0])]
        # print(position,label)
        return label
    
    def logicCheck(self,labelcheck):
        print(labelcheck)
        detectclass = ['black_4', 'black_5', 'black_6', 'black_8', 'handle_big', 'handle_small', 'whitebox']
        # detectclass = ['black_4', 'black_5', 'black_6', 'black_8', 'handle_big', 'handle_small', 'nobox' ,'whitebox']
        for i in labelcheck:
            idx = detectclass.index(i)
            print(idx)
    
    def checklistData(self,handle):
        data = []
        for check in range(3):
            res = self.checklist.getChecklistData(handle)
        # if res is not None:
        try: 
            checklist = (res[f"{handle}"])
        except:
            checklist = None
        # print(checklist)
        if checklist is not None:
            for i,j in enumerate(checklist):
                data.append([handle,j["LEFT_CASSETE"],j["RIGHT_CASSETE"]])
            return data
        else:
            return None

        # print((labelcheck[0]).split(' ',1)[0])

    def logicAnalysis(self,res):
        self.pos = []
        # res = res
        lenres = len(res)
        if(lenres < 3):
            return False
        elif (lenres == 3):
            for i , j in enumerate(res):
                res_1 = []
                label = []    
                # print(i," : ",j)
                for k in range(lenres-1):
                    res_1.append(j[k])
                for l in res:
                    label.append(l[lenres-1])

                position = self.findIntersectArea(res_1)
            # print(position)
            # print(label)
            relabelpos = self.rearrangeList(position,label)
            print(relabelpos)
            handle = relabelpos[0]
            data = self.checklistData(handle)
            if data is not None:
            # print(data)
                for checklist in data:
                    # print(checklist)
                    if relabelpos == checklist:
                        print(f'Setup is Correct {checklist}')
                        return True
                    elif 'nobox' in relabelpos:
                        print('nobox in list')
                        return True
            else:
                return None
        else:
            return False
        return False
            
        # self.logicCheck(relabelpos)

def DrawRectangle(frame3, R1, C1, R2, C2):
    start_point = (C1, R1)
    end_point = (C2, R2)
    color = (0, 255, 0)
    thickness = 3
    return cv.rectangle(cv.cvtColor(frame3, cv.COLOR_GRAY2BGR), start_point, end_point, color, thickness)

def drawrect(path,start1,end1,start2,end2):
    img = cv.imread(path)
    color1 = (225,0,0)
    color2 = (0,225,0)
    thickness = 2
    img = cv.rectangle(img, start1, end1, color1, thickness)
    img = cv.rectangle(img,start2,end2,color2,thickness)

    img = cv.resize(img,(0,0),fx=0.5, fy=0.5) 
    # cv.imshow('rect',img)
    # cv.waitKey(0)

if __name__=='__main__':

    Proc = Analysis()
    
    # res = [((24, 321), (916, 1078), 'nobox 0.96'),((861, 8), (1065, 353), 'handle_small 0.93'), ((1007, 311), (1914, 1080), 'nobox 0.97')]
    res = [[[740, 13], [1190, 504], 'handle_big 0.83'], [[16, 314], [921, 1077], 'nobox 0.95'], [[1053, 275], [1914, 1072], 'black_8 0.96']]
    # res = [((737, 0), (1216, 502), 'handle_big 0.85'), ((16, 198), (916, 1080), 'whitebox 0.86'), ((1010, 260), (1914, 1080), 'black_8 0.93')]
    # res = [[[735, 0], [1214, 502], "handle_big 0.85"], [[9, 278], [888, 1080], "black_8 0.90"], [[1010, 257], [1914, 1080], "black_8 0.92"]]
    # res = [((738, 0), (1215, 506), 'handle_big 0.85'), ((14, 276), (904, 1080), 'black_8 0.88'), ((1010, 224), (1905, 1080), 'black_8 0.90')]
    # res = [((16, 202), (920, 1080), 'whitebox 0.86'), ((740, 0), (1213, 502), 'handle_big 0.86'), ((1006, 261), (1914, 1080), 'black_8 0.93')]
    # res = [((740, 0), (1213, 502), 'handle_big 0.86'), ((1006, 261), (1914, 1080), 'black_8 0.93')]
    # res = [[[7, 219], [929, 1080], "whitebox 0.52"], [[742, 0], [1211, 504], "handle_big 0.86"], [[1022, 280], [1918, 1080], "black_8 0.95"]]
    p = Proc.logicAnalysis(res)
    print(p)

    '''
    # res = [((989, 54), (1646, 934), 'handle_big 0.86'), ((13, 612), (1233, 1798), 'black_8 0.91'), ((1358, 592), (2583, 1765), 'black_8 0.92')]

    # path = r'D:\fern\project_Fern\Backgrinding_jetson\BackGrinding_check\5.bmp'
    # start1 = (989,54)
    # end1 = (1646,934)
    # start2 = (485,7)
    # end2 = (2095,865)
    # drawrect(path,start1,end1,start2,end2)
    '''