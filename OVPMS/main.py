from fastapi import FastAPI, Body, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from pathlib import Path

from OVPMS.auth import verify_google_token
from OVPMS.database import engine, Base, get_db
from OVPMS.crud import get_or_create_user
from OVPMS.dependencies import require_admin
from OVPMS.security import create_access_token
from OVPMS import models

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="OVPMS Backend",
    version="0.1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


templates = Jinja2Templates(
    directory=BASE_DIR / "OVPMS" / "pages"
)


@app.post("/auth/google")
def google_login(
    token: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    print("STEP 1 ok")

    user_info = verify_google_token(token)
    print("USER INFO", user_info)

    google_id = user_info.get("sub")
    print("GOOGLE ID:", google_id)

    if not google_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google token payload",
        )

    email = user_info.get("email")
    name = user_info.get("name")
    picture = user_info.get("picture")

    user = get_or_create_user(
        db=db,
        google_id=google_id,
        email=email,
        name=name,
        picture=picture,
    )

    print("USER CREATED", user)

   
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
        }
    )

    
    return {
        "status": "success",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        },
    }


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/admin/test")
def admin_test(current_user=Depends(require_admin)):
    return {
        "message": f"Welcome Admin {current_user.email}"
    }