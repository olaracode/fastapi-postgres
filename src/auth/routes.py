from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.auth.crud import create_user, get_user_by_email, validate_password
from src.auth.schemas import UserCreate, UserInDB
from src.db.utils import get_db
from src.auth.jwt import get_current_user, create_access_token, Token, get_refresh_user

router = APIRouter()


@router.post("/register", response_model=UserInDB)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)


@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: Session = Depends(get_db)):
    def default_message():
        # Give a generic error message to avoid user enumeration
        raise HTTPException(
            status_code=400, detail="Invalid email or password")

    db_user = get_user_by_email(db, user.email)
    if not db_user:
        default_message()
    if not validate_password(db, user.email, user.password):
        default_message()

    access_token = create_access_token(
        data={"user": {"email": db_user.email, "id": db_user.id}})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh-token", response_model=Token)
async def refresh_token(
    current_user: dict = Depends(get_refresh_user)
):
    access_token = create_access_token(
        data={"email": current_user["email"], "id": current_user["id"]}
    )
    return access_token


@router.get("/me", response_model=UserInDB)
async def me(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_user = get_user_by_email(db, current_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
