from pydantic import BaseModel

class BGChecklist_model(BaseModel):
    HANDLE_TYPE: str
    LEFT_CASSETE: str
    RIGHT_CASSETE: str


class BGChecklist_tablemodel(BaseModel):
    ITEM : int
    HANDLE_TYPE: str
    LEFT_CASSETE: str
    RIGHT_CASSETE: str
    UPDATEDATE : str
    ACTIVEFLAG : bool
