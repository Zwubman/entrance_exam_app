from fastapi import APIRouter, Depends, UploadFile, File, Body
from app.config.database import get_db
from app.util.token import auth_checker
from app.schema.exam import ExamSearch, ExamSubmit
from app.router.chat import get_profile
from app.controller import exam

router = APIRouter(tags=['Exam Routers'], prefix='/exams')

@router.post('/', dependencies=[Depends(auth_checker)])
async def insert_new_exam(year: str = Body(...), subject: str = Body(...), extra_data: str = Body(None), file: UploadFile = File(...), db = Depends(get_db)):
    return await exam.insert_new_exam(year, subject, extra_data, file, db)

@router.get('/', dependencies=[Depends(auth_checker)])
def get_all_exams(limit: int = 25, next_page: str = None):
    return exam.get_all_exams(limit, next_page)

@router.get('/{exam_id}', dependencies=[Depends(auth_checker)])
def get_exam(exam_id):
    return exam.get_exam(exam_id)

@router.delete('/{exam_id}', dependencies=[Depends(auth_checker)])
def delete_exam(exam_id):
    return exam.delete_exam(exam_id)

@router.post('/search')
def search_exam(req: ExamSearch):
    return exam.search_exam(req)

@router.post('/submit')
def submit_exam(req: ExamSubmit):
    return exam.submit_exam(req)

@router.post('/new-chat')
def create_new_chat_from_exam(req: ExamSubmit, profile = Depends(get_profile), db = Depends(get_db)):
    return exam.create_new_chat_from_exam(req, profile, db)