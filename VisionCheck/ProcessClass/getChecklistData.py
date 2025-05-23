import requests
import json

class ChecklistData:
    def __init__(self) -> None:
        self.serverPath = "http://10.151.27.1:8082/Backgrinding_checklist"
    
    def getChecklistData(self,handle):
        # handle = 'handle_small'
        try:
            url = f"{self.serverPath}/{handle}"
            response = requests.request("GET", url)
            if response.status_code == 200:
                return json.loads(response.text)
        except:
            pass

if __name__=="__main__":
    proc = ChecklistData()
    listhandle = ['handle_small', 'whitebox', 'black_6']
    handle = listhandle[0]
    res = proc.getChecklistData(handle)
    data = (res[f"{handle}"])
    # print(data)
    for i,j in enumerate(data):
        # print(i,j)
        print(j["LEFT_CASSETE"],j["RIGHT_CASSETE"])
        
    # # for key, value in res.items():
    # for value in res:
    #     for i in value[f'{handle}']:
    #         print(i['LEFT_CASSETE'],i['RIGHT_CASSETE'])