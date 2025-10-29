from app.schema.feedback import FeedbackCreate
from sqlalchemy.orm import Session
from app.model.feedback import Feedback
from fastapi import HTTPException, status
from uuid import UUID

def submit_feedback(req: FeedbackCreate, db: Session):
    if req.rate < 0 or req.rate > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Rate is must be between 0 to 5'
        )
    
    new_feedback = Feedback(
        comment=req.comment,
        rate=req.rate
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return "Submitted"

def get_all_feedbacks(limit: int, page: int, db: Session):
    limit = 1 if limit < 1 else limit
    page = 1 if page < 1 else page
    offset = (page - 1) * limit
    total = db.query(Feedback).count()

    feedbacks = db.query(Feedback).limit(limit).offset(offset).all()
    return {
        'feedbacks': feedbacks,
        'page': page,
        'limit': limit,
        'total': total
    }

def get_feedback(feedback_id: UUID, db: Session):
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Feedback not found'
        )
    
    return feedback