from fastapi import APIRouter, Depends
from app.schema.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controller import user
from app.util.token import auth_checker

router = APIRouter(tags=['User Routers'], prefix='/users')

@router.post('/register')
def register(req: UserCreate, db: Session = Depends(get_db)):
    return user.register(req, db)

@router.post('/login')
def login(req: UserLogin, db: Session = Depends(get_db)):
    return user.login(req, db)

@router.put('/me')
def update_my_profile(id = Depends(auth_checker)):
    return id

@router.get('/me')
def get_my_profile():
    pass

@router.get('/')
def get_all_users():
    pass

@router.get('/{id}')
def get_user_profile():
    pass

@router.delete('/{id}')
def delete_user():
    pass

@router.delete('/me')
def delete_my_profile():
    pass

@router.post('/{id}')
def add_admin_role():
    pass