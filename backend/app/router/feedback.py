from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.util.token import auth_checker

router = APIRouter(tags=['Feedback Routers'], prefix='/feedbacks')

@router.post('/')
def submit_feedback():
    pass

@router.get('/', dependencies=[Depends(auth_checker)])
def get_all_feedbacks():
    pass

@router.get('/{feedback_id}', dependencies=[Depends(auth_checker)])
def get_feedback():
    pass