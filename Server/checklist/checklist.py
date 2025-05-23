from datetime import datetime, date
from fastapi import FastAPI, requests, Depends, Response, status, APIRouter
from typing import List

from sqlalchemy import and_, desc, asc
from starlette.background import BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from .checklistdb import BGChecklist,session
from .checklistmodel import BGChecklist_model,BGChecklist_tablemodel

from pydantic.datetime_parse import datetime
import uvicorn

checklist = APIRouter(
    prefix="/Backgrinding_checklist",
    tags=["CHECKLIST"],
    responses={200: {"message": "OK"}}
)

def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()

@checklist.get("")
async def Checklist(db: session = Depends(get_db)):
    bg = db.query(BGChecklist).filter(and_(BGChecklist.ACTIVEFLAG == True,BGChecklist.HANDLE_TYPE.isnot(None))).order_by(asc(BGChecklist.HANDLE_TYPE)).all()
    res = {}
    for i in bg:
        key = i.HANDLE_TYPE
        try:
            if(len(res[key])>0): 
                pass
            else:
                res[key] = []
        except:
            res[key] = []      
        resdic = {}
        resdic['LEFT_CASSETE'] = i.LEFT_CASSETE
        resdic['RIGHT_CASSETE'] = i.RIGHT_CASSETE
        # resdic['UPDATEDATE'] = i.UPDATEDATE
        res[key].append(resdic)
    return res

@checklist.get("/{HANDLE_TYPE}")
async def Checklistbyhandle(HANDLE_TYPE, db: session = Depends(get_db)):
    bg = db.query(BGChecklist).filter(and_(BGChecklist.ACTIVEFLAG == True, BGChecklist.HANDLE_TYPE == HANDLE_TYPE)).order_by(
        asc(BGChecklist.HANDLE_TYPE)).all()
    res = {}
    for i in bg:
        key = i.HANDLE_TYPE
        try:
            if (len(res[key]) > 0):
                pass
            else:
                res[key] = []
        except:
            res[key] = []
        resdic = {}
        # resdic['HANDLE_TYPE'] = i.HANDLE_TYPE
        resdic['LEFT_CASSETE'] = i.LEFT_CASSETE
        resdic['RIGHT_CASSETE'] = i.RIGHT_CASSETE
        res[key].append(resdic)
    return res

@checklist.post("")
async def PostChecklist(checklist:BGChecklist_model,db: session = Depends(get_db)):
    BG = BGChecklist()
    BG.HANDLE_TYPE = checklist.HANDLE_TYPE
    BG.LEFT_CASSETE = checklist.LEFT_CASSETE
    BG.RIGHT_CASSETE = checklist.RIGHT_CASSETE
    BG.UPDATEDATE = datetime.now()
    db.add(BG)
    db.commit()
    return {"Code: Success"}


