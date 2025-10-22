from fastapi import APIRouter, Depends
from app.schema.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controller import user
from app.util.token import auth_checker

router = APIRouter(tags=['Exam Routers'], prefix='/exams')

@router.post('/', dependencies=[Depends(auth_checker)])
def insert_exam():
    pass

@router.delete('/{exam_id}', dependencies=[Depends(auth_checker)])
def delete_exam():
    pass

@router.get('/')
def get_all_exam():
    pass

@router.get('/{exam_id}')
def get_one_exam():
    pass