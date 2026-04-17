@echo off
REM 5G Nexus Slicer - Backend Server Startup
echo Starting 5G Nexus Slicer Backend...
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
