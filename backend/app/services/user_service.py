from sqlalchemy.orm import Session
from fastapi import HTTPException
from backend.app.models.user_model import User
from backend.app.schemas.user_schema import UserCreate
from backend.app.utils.id_service import unique_id


def create_user(db: Session, user_data: UserCreate):
    try:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        user_id = unique_id(db, User, "U")

        new_user = User(
            id=user_id,
            name=user_data.name,
            email=user_data.email
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    except Exception:
        db.rollback()
        raise