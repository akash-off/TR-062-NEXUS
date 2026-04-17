# 5G Nexus Slicer - Project Structure

## Directory Organization

```
5g-nexus-slicer/
├── backend/                          # Backend API & Services
│   ├── app/
│   │   ├── api/                     # API routes
│   │   │   ├── index.py
│   │   │   └── routes.py
│   │   ├── core/                    # Core configuration
│   │   │   ├── config.py
│   │   │   └── __init__.py
│   │   ├── models/                  # ML Models
│   │   │   ├── rl_agent.py
│   │   │   └── __init__.py
│   │   ├── schemas/                 # Data schemas
│   │   │   ├── traffic.py
│   │   │   └── __init__.py
│   │   ├── services/                # Business logic
│   │   │   ├── allocator.py
│   │   │   ├── sla_monitor.py
│   │   │   └── __init__.py
│   │   └── main.py                  # FastAPI app entry point
│   ├── simulator/                   # 5G Network Simulator
│   │   ├── simulator.py
│   │   └── __init__.py
│   └── requirements.txt             # Python dependencies
│
├── frontend/                        # Frontend UI (React)
│   ├── public/                      # Static files
│   ├── src/                         # React source code
│   ├── package.json                 # Node dependencies
│   └── README.md
│
├── docs/                            # Documentation
│   ├── CODE_VERIFICATION_REPORT.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── PROJECT_STRUCTURE.md
│   └── API_REFERENCE.md
│
├── tests/                           # Test files
│   └── prototype_demo.py
│
├── .venv/                           # Python virtual environment
├── .git/                            # Git repository
│
├── start-backend.bat                # Quick start - Backend only (Windows)
├── start-backend.sh                 # Quick start - Backend only (Linux/Mac)
├── start-all.bat                    # Start both services (Windows)
│
├── README.md                        # Project README
├── QUICKSTART.md                    # Quick start guide
└── requirements.txt                 # Root requirements (legacy)
```

## Getting Started

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

**Backend URLs:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

**Frontend URL:**
- Application: http://localhost:3000

### Run All Services (Windows)
```bash
start-all.bat
```

### Run Backend Only (Windows)
```bash
start-backend.bat
```

## Project Components

### Backend
- **API**: FastAPI REST endpoints for network slicing
- **Simulator**: 5G network traffic simulator
- **Services**: Resource allocation, SLA monitoring
- **Models**: Reinforcement learning agent
- **Schemas**: Request/response validation

### Frontend
- React-based dashboard
- Real-time network metrics visualization
- Slice management interface
- Configuration dashboard

### Documentation
- Implementation details
- API reference
- Code verification reports
