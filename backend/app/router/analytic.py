from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.util.token import auth_checker

router = APIRouter(tags=['Analytic Routers'], prefix='/analytics')

@router.get('/', dependencies=[Depends(auth_checker)])
def get_analytics():
    pass