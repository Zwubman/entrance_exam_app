from fastapi import APIRouter, Depends
from app.config.database import get_db

router = APIRouter(tags=['Profile Routers'], prefix='/profiles')

@router.post('/')
def create_profile():
    pass

@router.put('/')
def update_profile():
    pass