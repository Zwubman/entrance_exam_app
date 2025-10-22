from fastapi import APIRouter, Depends
from app.schema.user import UserCreate, UserLogin
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.controller import user
from app.util.token import auth_checker

router = APIRouter(tags=['Profile Routers'], prefix='/profile')

@router.post('/')
def create_profile():
    pass

@router.put('/')
def update_profile():
    pass