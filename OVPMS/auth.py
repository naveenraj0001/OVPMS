from fastapi import HTTPException
from google.oauth2 import id_token
from google.auth.transport import requests

from OVPMS.config import GOOGLE_CLIENT_ID

from sqlalchemy.orm import Session
from fastapi import Depends

from OVPMS.database import get_db
from OVPMS.crud import get_or_create_user


def verify_google_token(token: str) -> dict:
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        return {
            "sub": idinfo["sub"],
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
            "google_id": idinfo.get("sub"),
            "picture": idinfo.get("picture"),
            "email_verified": idinfo.get("email_verified"),
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
