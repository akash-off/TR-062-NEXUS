# Quick Start Guide

## 1. Install Dependencies (First Time Only)

Open terminal in project root (`e:\5g Nexus Slicer`):

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 pydantic-2.5.0 ...
```

## 2. Start the Backend API

Terminal 1:

```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000/
INFO:     Application startup complete
```

## 3. Open API Documentation

Visit in browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 4. Test Health Check

Terminal 2 (new):

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": 1234567890.0
}
```

## 5. Run Traffic Simulator

Terminal 3 (new):

```bash
python -m simulator.simulator
```

Output:
```
INFO:     Starting simulation for 120s (batch every 1.0s, 10 items/batch)
INFO:     Batch batch_000001 sent successfully (10 items)
INFO:     Total items sent: 10
...
```

## 6. Monitor Predictions

Terminal 2:

```bash
# Get prediction for URLLC slice
curl http://localhost:8000/api/predict/slice_urllc

# Get traffic statistics
curl http://localhost:8000/api/traffic/statistics

# List all slices
curl http://localhost:8000/api/slices
```

## 7. View API Documentation

- Try endpoints in Swagger UI: http://localhost:8000/docs
- Click "Try it out" on any endpoint
- See live responses

---

## Project Layout

```
app/
├── main.py              <- FastAPI app
├── api/routes.py        <- API endpoints
├── models/rl_agent.py   <- Mock RL agent
├── services/            <- Business logic
│   ├── allocator.py     <- Bandwidth allocation
│   └── sla_monitor.py   <- SLA validation
├── schemas/traffic.py   <- Data models
└── core/config.py       <- Configuration

simulator/
└── simulator.py         <- Traffic generator
```

---

## Key Files Explained

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application initialization & routes |
| `app/core/config.py` | Slice definitions & settings |
| `app/models/rl_agent.py` | Rule-based allocation logic |
| `app/services/allocator.py` | Bandwidth management |
| `app/services/sla_monitor.py` | SLA compliance checking |
| `app/schemas/traffic.py` | Pydantic data models |
| `simulator/simulator.py` | Traffic simulation engine |
| `requirements.txt` | Python dependencies |

---

## API Endpoints Summary

### Info
- `GET /` - System info
- `GET /health` - Health check
- `GET /api/slices` - List slices

### Traffic
- `POST /api/ingest` - Ingest traffic batch
- `GET /api/traffic/statistics` - Traffic stats
- `GET /api/traffic/buffer` - View buffer

### Predictions
- `GET /api/predict/{slice_id}` - Get allocation

### Real-time
- `WS /api/stream` - WebSocket stream

---

## Example Commands

```bash
# 1. Check API health
curl http://localhost:8000/health

# 2. List configured slices
curl http://localhost:8000/api/slices

# 3. Get traffic statistics
curl http://localhost:8000/api/traffic/statistics

# 4. Request allocation prediction
curl http://localhost:8000/api/predict/slice_urllc

# 5. Get recent traffic items
curl http://localhost:8000/api/traffic/buffer?limit=5
```

---

## Stopping Services

- Press `Ctrl+C` in each terminal
- All data is cleared (in-memory only)

---

## Customization

### Change Slice Configuration

Edit `app/core/config.py`:

```python
"slice_embb": SliceConfig(
    slice_id="slice_embb",
    slice_type="eMBB",
    max_bandwidth=1000.0,           # <- Change this
    min_latency_threshold=50.0,     # <- Or this
    # ...
)
```

### Modify Simulator

Edit `simulator/simulator.py`:

```python
await simulator.simulate_continuous(
    duration_seconds=120,           # Duration
    batch_interval_seconds=1.0,     # Batch frequency
    batch_size=10,                  # Items per batch
    pattern=TrafficPattern.RANDOM,  # Pattern type
)
```

### Change API Port

```bash
uvicorn app.main:app --reload --port 8001
```

---

## Debugging

### Enable Debug Logging

```python
# In app/main.py, change:
logging.basicConfig(level=logging.DEBUG)  # Instead of INFO
```

### View Detailed Errors

Add `?debug=true` to API calls or check console output.

---

## Next Steps

1. ✓ Backend running locally
2. Integrate with frontend (WebSocket at `/api/stream`)
3. Build real ML model
4. Add database persistence
5. Deploy to production

---

Enjoy building the 5G Network Slicing System!
