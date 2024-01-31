from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from src.db.operations.user_crud import create_user, get_user_by_email
from src.schemas.user import UserCreate, UserInDB
from src.db.utils import get_db

router = APIRouter()

@router.post("/register", response_model=UserInDB)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)
