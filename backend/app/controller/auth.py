from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.model.user import User
from app.util.security import verify_pswd
from app.util.token import create_access_token
from fastapi import HTTPException, status

def get_login_token(req: OAuth2PasswordRequestForm, db: Session):
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

    access_token = create_access_token({"id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}