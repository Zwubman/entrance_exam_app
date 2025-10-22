from sqlalchemy.orm import Session
from app.schema.user import UserCreate, UserLogin
from app.model.user import User
from fastapi import HTTPException, status
from app.util.security import hash_pswd, verify_pswd
from app.util.token import create_access_token

def register(req: UserCreate, db: Session):
    _user = db.query(User).filter(User.email == req.email).first()
    if _user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User with this email already exists'
        )

    hashed_password = hash_pswd(req.password)
    user = User(
        username=req.username,
        email=req.email,
        password=hashed_password,
        grade=req.grade
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "User registered successfully",
        "data": user
    }

def login(req: UserLogin, db: Session):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User with this email does not exist'
        )
    
    if not verify_pswd(req.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )

    token = create_access_token({'id': str(user.id)})
    return {
        "success": True,
        "message": "User logged in successfully",
        "data": user,
        "token": token
    }