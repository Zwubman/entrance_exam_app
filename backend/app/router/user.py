from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controller import user
from app.schema.user import AddAdmin, UserLogin, UserUpdate, DeleteResponse
from app.config.database import get_db
from app.util.token import auth_checker
from uuid import UUID

router = APIRouter(tags=["User Routers"], prefix="/users")


@router.post("/", dependencies=[Depends(auth_checker)])
def add_new_admin(req: AddAdmin, db: Session = Depends(get_db)):
    return user.add_new_admin(req, db)

@router.get("/create-super-admin")
def create_default_super_admin(db: Session = Depends(get_db)):
    return user.create_default_super_admin(db)

@router.post("/login")
def login(req: UserLogin, db: Session = Depends(get_db)):
    return user.login(req, db)


@router.put("/me", dependencies=[Depends(auth_checker)])
def update_my_profile(req: UserUpdate, db: Session = Depends(get_db), current_user=Depends(auth_checker)):
    return user.update_my_profile(req, db, current_user)


@router.get("/me", dependencies=[Depends(auth_checker)])
def get_my_profile(current_user=Depends(auth_checker)):
    return user.get_my_profile(current_user)


@router.get("/", dependencies=[Depends(auth_checker)])
def get_all_users(db: Session = Depends(get_db), current_user=Depends(auth_checker)):
    return user.get_all_users(db, current_user)


@router.delete("/{user_id}", dependencies=[Depends(auth_checker)])
def delete_user(user_id: str, db: Session = Depends(get_db), current_user=Depends(auth_checker)):
    return user.delete_user(UUID(user_id), db, current_user)


@router.delete("/me", response_model=DeleteResponse, dependencies=[Depends(auth_checker)])
def delete_my_profile_route(db: Session = Depends(get_db), current_user=Depends(auth_checker)):
    return user.delete_my_profile(db, current_user)
