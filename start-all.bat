@echo off
REM 5G Nexus Slicer - Frontend & Backend Startup
echo Starting 5G Nexus Slicer...
echo.
echo Backend will run on: http://localhost:8000
echo API Docs on: http://localhost:8000/docs
echo Frontend will run on: http://localhost:3000
echo.
start "" cmd /k "cd backend && python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
timeout /t 3
start "" cmd /k "cd frontend && npm start"
