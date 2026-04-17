"""
Vercel ASGI Entry Point for 5G Network Slicing FastAPI Backend.
This file is used by Vercel's @vercel/python builder to identify the app.
"""
from main import app

__all__ = ["app"]

