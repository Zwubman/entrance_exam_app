from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.util.token import auth_checker

router = APIRouter(tags=['User Routers'], prefix='/users')

@router.post('/', dependencies=[Depends(auth_checker)])
def add_new_admin():
    pass

@router.post('/login')
def login():
    pass

@router.put('/me', dependencies=[Depends(auth_checker)])
def update_my_profile():
    pass

@router.get('/me', dependencies=[Depends(auth_checker)])
def get_my_profile():
    pass

@router.get('/', dependencies=[Depends(auth_checker)])
def get_all_users():
    pass

@router.delete('/{user_id}', dependencies=[Depends(auth_checker)])
def delete_user():
    pass

@router.delete('/me', dependencies=[Depends(auth_checker)])
def delete_my_profile():
    pass