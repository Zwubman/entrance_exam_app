from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db 
from app.controller import profile
from app.schema.profile import ProfileCreate, ProfileUpdate
from app.util.token import auth_checker


router = APIRouter(tags=['Profile Routers'], prefix='/profiles')

@router.post("/")
def create_my_profile(req: ProfileCreate, db: Session = Depends(get_db)):
    return profile.create_my_profile(req, db)

@router.put("/", dependencies=[Depends(auth_checker)])
def update_my_profile(req: ProfileUpdate, db: Session = Depends(get_db), current_profile=Depends(auth_checker)):
    return profile.update_my_profile(req, db, current_profile)