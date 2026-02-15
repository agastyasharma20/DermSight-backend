from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, analyze

app = FastAPI(
    title="DermSight API",
    description="AI-powered dermatology triage system",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://derm-sight-frontend.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "DermSight Backend Running"}
from app.db.database import engine, Base
from app.models import models
from app.models.case import Case

Base.metadata.create_all(bind=engine)
