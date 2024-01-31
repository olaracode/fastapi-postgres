from fastapi import FastAPI, HTTPException, Depends

from src.db.database import engine, SessionLocal
from src.routes.user import router as UserRouter

app = FastAPI()
app.include_router(UserRouter, prefix="/user", tags=["user"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
