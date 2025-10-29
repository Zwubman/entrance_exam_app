from fastapi import APIRouter, Depends
from app.config.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.schema.auth import AuthTokenResponse
from app.controller import auth

router = APIRouter(tags=['Auth Routers'], prefix='/auth')

@router.post('/login')
def login():
    pass

@router.post("/token", response_model=AuthTokenResponse)
async def get_login_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    return auth.get_login_token(form_data, db)