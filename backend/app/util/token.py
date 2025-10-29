import jwt
from datetime import datetime, timedelta
from app.config.setting import settings
from fastapi import HTTPException, status, Depends
from app.config.database import get_db
from sqlalchemy.orm import Session
from app.model.user import User
from fastapi.security import OAuth2PasswordBearer
from uuid import UUID

oauth2 = OAuth2PasswordBearer(tokenUrl='auth/token')

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=365)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm='HS256')

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Token is invalid or expired'
        )

def auth_checker(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
        user_id: str = payload.get('id')
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )
        user = db.query(User).filter(
            User.id == UUID(user_id),
            User.is_deleted == False
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )