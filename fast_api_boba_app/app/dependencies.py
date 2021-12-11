from fastapi import Header, HTTPException
from typing import Generator
from app.db.session import SessionLocal

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


## TODO: add user login stuff