from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.schema.feedback import FeedbackCreate
from app.controller import feedback
from app.util.token import auth_checker
from uuid import UUID

router = APIRouter(tags=['Feedback Routers'], prefix='/feedbacks')

@router.post('/')
def submit_feedback(req: FeedbackCreate, db = Depends(get_db)):
    return feedback.submit_feedback(req, db)

@router.get('/', dependencies=[Depends(auth_checker)])
def get_all_feedbacks(limit: int = 25, page: int = 1, db = Depends(get_db)):
    return feedback.get_all_feedbacks(limit, page, db)

@router.get('/{feedback_id}', dependencies=[Depends(auth_checker)])
def get_feedback(feedback_id, db = Depends(get_db)):
    return feedback.get_feedback(UUID(feedback_id), db)