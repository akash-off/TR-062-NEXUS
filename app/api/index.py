from fastapi import FastAPI
from app.main import app as main_app

# Create a wrapper app for Vercel
app = FastAPI()

# Root route (important for avoiding 404)
@app.get("/")
def root():
    return {"message": "5G AI Backend Running on Vercel 🚀"}

# Mount your actual FastAPI app
app.mount("/", main_app)