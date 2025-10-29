from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.model.user import User
from app.util.token import create_access_token
from fastapi import HTTPException, status

def get_login_token(req: OAuth2PasswordRequestForm, db: Session):
    user = db.query(User).filter((User.email == req.username) & (User.is_deleted == False)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invalid credential'
        )
    access_token = create_access_token({'id': str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}