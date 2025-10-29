from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.model.profile import Profile
from app.schema.profile import ProfileCreate, ProfileUpdate, ProfileResponse

def create_my_profile(req: ProfileCreate, db: Session):
    # Check if a profile with the same device_id already exists
    existing_profile = db.query(Profile).filter(Profile.device_id == req.device_id).first()
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Profile with this device ID already exists"
        )

    # Create new profile
    profile = Profile(
        device_id=req.device_id,
        category=req.category,
        stream=req.stream
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {
        "success": True,
        "message": "Profile created successfully",
        "data": ProfileResponse.from_orm(profile)
    }

def update_my_profile(req: ProfileUpdate, db: Session, current_profile: Profile):
    # Check for unique device_id if it's being updated
    if req.device_id and req.device_id != current_profile.device_id:
        existing = db.query(Profile).filter(Profile.device_id == req.device_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another profile with this device ID already exists"
            )
        current_profile.device_id = req.device_id

    # Update category if provided
    if req.category:
        current_profile.category = req.category

    # Update stream if provided
    if req.stream:
        current_profile.stream = req.stream

    db.commit()
    db.refresh(current_profile)

    return {
        "success": True,
        "message": "Profile updated successfully",
        "data": ProfileResponse.from_orm(current_profile)
    }