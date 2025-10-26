from fastapi import APIRouter, Depends
from app.config.database import get_db
from app.util.token import auth_checker

router = APIRouter(tags=['Upload Routers'], prefix='/uploads')

@router.get('/', dependencies=[Depends(auth_checker)])
def get_all_uploaded_sheet():
    pass

@router.get('/{upload_id}', dependencies=[Depends(auth_checker)])
def get_uploaded_sheet():
    pass

@router.get('/{upload_id}/insert-exam', dependencies=[Depends(auth_checker)])
def insert_exam_from_sheet():
    pass

@router.delete('/{upload_id}', dependencies=[Depends(auth_checker)])
def delete_uploaded_sheet():
    pass

@router.delete('/{upload_id}/force', dependencies=[Depends(auth_checker)])
def force_delete_uploaded_sheet():
    pass