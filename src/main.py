from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from src.database import engine, SessionLocal

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
