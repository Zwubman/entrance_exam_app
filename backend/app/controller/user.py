from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schema.user import AddAdmin, UserLogin, UserUpdate, UserResponse
from app.model.user import User
from app.util.security import hash_pswd, verify_pswd
from app.util.token import create_access_token


def add_new_admin(req: AddAdmin, db: Session):
    existing_user = db.query(User).filter(User.email == req.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User with this email already exists"
            )

    hashed_password = hash_pswd(req.password)
    new_admin = User(
        email=req.email, 
        password=hashed_password, 
        role=req.role or "admin"
        )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {
        "success": True,
        "message": "Admin created successfully",
        "data": UserResponse.from_orm(new_admin)
    }


def login(req: UserLogin, db: Session):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User with this email does not exist"
            )

    if not verify_pswd(req.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
            )

    token = create_access_token({"id": str(user.id)})
    return {
        "success": True,
        "message": "Login successful",
        "token": token,
        "data": UserResponse.from_orm(user)
    }


def update_my_profile(req: UserUpdate, db: Session, current_user: User):
    if req.email:
        existing_user = db.query(User).filter(User.email == req.email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Email already in use"
                )
        current_user.email = req.email

    if req.password:
        current_user.password = hash_pswd(req.password)

    db.commit()
    db.refresh(current_user)

    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": UserResponse.from_orm(current_user)
    }


def get_my_profile(current_user: User):
    return {
        "success": True,
        "message": "Profile retrieved successfully",
        "data": UserResponse.from_orm(current_user)
    }


def get_all_users(db: Session, current_user: User):
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only super admins can view all users"
            )

    users = db.query(User).filter(User.is_deleted == False).all()
    response = [UserResponse.from_orm(u) for u in users]
    return {"success": True, "count": len(response), "data": response}


def delete_user(user_id: str, db: Session, current_user: User):
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Only super admins can delete users"
            )

    user = db.query(User).filter(User.id == user_id, User.is_deleted == False).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found or already deleted"
            )

    user.soft_delete()
    db.commit()

    return {
        "success": True, 
        "message": f"User with ID {user_id} soft deleted successfully"
        }


def delete_my_profile(db: Session, current_user: User):
    user = db.query(User).filter(User.id == current_user.id, User.is_deleted == False).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found or already deleted"
            )

    user.soft_delete()
    db.commit()
    return {
        "success": True, 
        "message": "Your profile has been successfully deleted."
        }
