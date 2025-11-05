from fastapi import APIRouter, Depends, Query
from app.config.database import get_db
from app.util.token import auth_checker
from app.schema.exam import ExamInsert
from app.controller import uploaded_sheet as sheet

router = APIRouter(tags=['Upload Routers'], prefix='/uploads')

@router.get('/', dependencies=[Depends(auth_checker)])
def get_all_uploaded_sheet():
    return sheet.get_all_uploaded_sheet()

@router.post('/insert-exam', dependencies=[Depends(auth_checker)])
def insert_exam_from_sheet(req: ExamInsert, url: str = Query(...)):
    return sheet.insert_exam_from_sheet(url, req)

@router.delete('/', dependencies=[Depends(auth_checker)])
def force_delete_uploaded_sheet(url: str):
    return sheet.force_delete_uploaded_sheet(url)