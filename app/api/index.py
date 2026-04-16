from fastapi import FastAPI
from app.main import app as main_app

app = main_app

@app.get("/")
def root():
    return {"message": "5G AI Backend Running 🚀"}