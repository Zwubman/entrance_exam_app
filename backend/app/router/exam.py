from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.util.token import auth_checker

router = APIRouter(tags=['Exam Routers'], prefix='/exams')

@router.post('/', dependencies=[Depends(auth_checker)])
def insert_exam():
    pass

@router.get('/', dependencies=[Depends(auth_checker)])
def get_all_exams():
    pass

@router.get('/{exam_id}', dependencies=[Depends(auth_checker)])
def get_one_exam():
    pass

@router.put('/{exam_id}', dependencies=[Depends(auth_checker)])
def update_exam():
    pass

@router.delete('/{exam_id}', dependencies=[Depends(auth_checker)])
def delete_exam():
    pass

@router.get('/search')
def search_exam():
    pass

@router.post('/{exam_id}/submit')
def submit_exam():
    pass

@router.post('/{exam_id}/new-chat')
def create_new_chat_from_exam():
    pass