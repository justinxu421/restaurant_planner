from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.endpoints import business

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(business.router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
