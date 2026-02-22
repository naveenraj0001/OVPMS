from sqlalchemy.orm import Session
from OVPMS.models import User
from OVPMS.config import ADMIN_EMAILS, VENDOR_EMAILS


def get_user_by_google_id(db: Session, google_id: str):
    return db.query(User).filter(User.google_id == google_id).first()


def determine_role(email: str) -> str:
    if email in ADMIN_EMAILS:
        return "admin"
    elif email in VENDOR_EMAILS:
        return "vendor"
    return "user"


def create_user(
    db: Session,
    google_id: str,
    email: str,
    name: str,
    picture: str,
):
    role = determine_role(email)

    user = User(
        google_id=google_id,
        email=email,
        name=name,
        picture=picture,
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(
    db: Session,
    google_id: str,
    email: str,
    name: str,
    picture: str,
):
    user = get_user_by_google_id(db, google_id)
    new_role = determine_role(email)

    if user:
        if user.role != new_role:
            user.role = new_role
            db.commit()
            db.refresh(user)
        return user

    return create_user(db, google_id, email, name, picture)

