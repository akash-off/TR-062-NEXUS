from fastapi import FastAPI
from app.main import app as backend_app

# Vercel expects this variable name
app = backend_app