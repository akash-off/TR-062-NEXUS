# 5G Network Slicing Backend Prototype

AI-Driven Adaptive Network Slice Configuration System for 5G - Phase 1 (Local Development)

## Overview

This is a **runnable backend prototype** designed for local development in VS Code. It implements core components for adaptive network slice allocation using mock AI logic.

**Status**: Phase 1 (~30% completion) - Prototype working locally ✓

---

## Project Structure

```
5g Nexus Slicer/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py           # Configuration & slice definitions
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py           # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── rl_agent.py         # Mock RL agent (rule-based)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── allocator.py        # Resource allocation service
│   │   └── sla_monitor.py      # SLA compliance monitoring
│   └── schemas/
│       ├── __init__.py
│       └── traffic.py          # Pydantic models
├── simulator/
│   ├── __init__.py
│   └── simulator.py            # Traffic simulator
└── requirements.txt            # Python dependencies
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Backend

```bash
uvicorn app.main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 3. Access API

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

### 4. Run Traffic Simulator (New Terminal)

```bash
python -m simulator.simulator
```

The simulator will:
- Generate synthetic 5G traffic (eMBB, URLLC, mMTC)
- Send batches to the `/ingest` endpoint
- Display ingestion status

---

## API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | System information |
| GET | `/health` | Health check |
| GET | `/api/slices` | List configured slices |

### Traffic Ingestion

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ingest` | Ingest traffic batch |
| GET | `/api/traffic/statistics` | Traffic statistics |
| GET | `/api/traffic/buffer` | Get buffer contents |
| POST | `/api/clear-buffer` | Clear buffer |

### Predictions & Allocation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/predict/{slice_id}` | Get allocation prediction |

### Real-time Streaming

| Method | Endpoint | Description |
|--------|----------|-------------|
| WS | `/api/stream` | WebSocket for traffic stream |

---

## Components

### 1. **Configuration (core/config.py)**

Defines three network slices:

```python
{
  "slice_embb": {
    "type": "eMBB (Enhanced Mobile Broadband)",
    "max_bandwidth": 1000 Mbps,
    "min_latency": 50 ms,
    "priority": 2
  },
  "slice_urllc": {
    "type": "URLLC (Ultra-Reliable Low-Latency)",
    "max_bandwidth": 500 Mbps,
    "min_latency": 1 ms,
    "priority": 1 (highest)
  },
  "slice_mmtc": {
    "type": "mMTC (Massive IoT)",
    "max_bandwidth": 200 Mbps,
    "min_latency": 100 ms,
    "priority": 3
  }
}
```

### 2. **Mock RL Agent (models/rl_agent.py)**

**Rule-based allocation logic** (not actual ML):

- **URLLC (P1)**: High bandwidth priority, minimal latency buffer
- **eMBB (P2)**: Variable bandwidth, standard latency
- **mMTC (P3)**: Low bandwidth, flexible latency

Features:
- State normalization
- Priority-weighted allocation
- Action history tracking

### 3. **Resource Allocator (services/allocator.py)**

Manages bandwidth across slices:

- Priority-based allocation
- Bandwidth rebalancing
- Allocation history
- State snapshots

### 4. **SLA Monitor (services/sla_monitor.py)**

Validates SLA compliance:

- Latency threshold checking
- Throughput minimum validation
- Violation recording
- Statistics tracking

### 5. **Traffic Simulator (simulator/simulator.py)**

Generates synthetic 5G patterns:

- **eMBB**: High bandwidth, variable latency
- **URLLC**: Low latency, medium bandwidth
- **mMTC**: IoT patterns, high packet count

Patterns:
- `RANDOM`: Unpredictable variations
- `BURST`: Peak traffic events
- `STEADY`: Stable patterns

### 6. **API Routes (api/routes.py)**

FastAPI endpoints for:
- Traffic ingestion
- Prediction requests
- Statistics queries
- WebSocket streaming
- Buffer management

### 7. **Pydantic Schemas (schemas/traffic.py)**

Type-safe models:
- `TrafficDataItem`: Single traffic record
- `TrafficBatch`: Batch of items
- `AllocationDecision`: RL agent output
- `SLAStatus`: Compliance status
- `PredictionResponse`: Full prediction

---

## Example Usage

### 1. Ingest Traffic

```bash
curl -X POST http://localhost:8000/api/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "batch_id": "batch_001",
    "timestamp": 1234567890.0,
    "data": [
      {
        "timestamp": 1234567890.0,
        "slice_id": "slice_embb",
        "slice_type": "eMBB",
        "bandwidth_demand": 750.5,
        "latency_requirement": 45.2,
        "packet_count": 5000,
        "priority": 2
      }
    ]
  }'
```

### 2. Get Prediction

```bash
curl http://localhost:8000/api/predict/slice_urllc
```

**Response:**
```json
{
  "slice_id": "slice_urllc",
  "decision": {
    "slice_id": "slice_urllc",
    "allocated_bandwidth": 425.3,
    "priority_level": 1,
    "action_id": "action_1234567890",
    "confidence": 0.9456
  },
  "sla_status": {
    "slice_id": "slice_urllc",
    "is_compliant": true,
    "latency_ms": 0.85,
    "throughput_mbps": 52.3,
    "violation_reason": null
  },
  "timestamp": 1234567890.0
}
```

### 3. List Slices

```bash
curl http://localhost:8000/api/slices
```

### 4. Get Traffic Statistics

```bash
curl http://localhost:8000/api/traffic/statistics
```

---

## Key Features

✅ **Fully Functional Backend**
- FastAPI framework with type hints
- Async/await support
- CORS enabled

✅ **Mock AI Components**
- Rule-based RL agent (no ML training needed)
- Realistic state representation
- Confidence scoring

✅ **Production-Ready Patterns**
- Pydantic validation
- Error handling
- Logging
- WebSocket support

✅ **Traffic Simulation**
- 3 slice types (eMBB, URLLC, mMTC)
- 3 traffic patterns (random, burst, steady)
- Realistic latency/bandwidth values

✅ **Monitoring & Validation**
- SLA compliance checking
- Resource tracking
- Violation history

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| API Framework | FastAPI | 0.104.1 |
| ASGI Server | Uvicorn | 0.24.0 |
| Data Validation | Pydantic | 2.5.0 |
| Numerics | NumPy | 1.24.3 |
| Data Processing | Pandas | 2.1.1 |
| HTTP Client | HTTPX | 0.25.1 |
| Python | 3.10+ | Required |

---

## Development Notes

### Adding New Features

1. **New endpoint**: Add route to `app/api/routes.py`
2. **New model**: Add class to `app/schemas/traffic.py`
3. **New service**: Create in `app/services/`
4. **Configuration**: Update `app/core/config.py`

### Testing

All modules were tested and compile successfully:

```bash
# Verify all imports
python -c "from app.main import app; print('OK')"

# Compile all files
python -m py_compile app/**/*.py simulator/*.py
```

### Type Hints

All code uses full type annotations:

```python
def allocate_bandwidth(
    self, slice_id: str, requested_bandwidth: float, priority_level: int
) -> Tuple[bool, ResourceAllocation]:
    """..."""
```

---

## Limitations (Phase 1)

- ⚠️ Mock predictions (not ML-based)
- ⚠️ In-memory buffer only (no persistence)
- ⚠️ No authentication/authorization
- ⚠️ Single-node only (no multi-instance)
- ⚠️ No database integration

---

## Next Steps (Phase 2+)

- [ ] Real ML model training
- [ ] PostgreSQL/MongoDB integration
- [ ] Containerization (Docker)
- [ ] Prometheus metrics
- [ ] Kubernetes deployment
- [ ] Multi-node support
- [ ] Real 5G traffic integration
- [ ] Advanced SLA enforcement

---

## Troubleshooting

### Port 8000 Already in Use

```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

### ModuleNotFoundError

```bash
# Ensure PYTHONPATH includes project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Simulator Can't Connect

```bash
# Verify API is running on port 8000
curl http://localhost:8000/health
```

---

## License

Prototype for development purposes - All rights reserved

---

## Support

- **Docs**: http://localhost:8000/docs
- **Schema Validation**: Auto-validated by Pydantic
- **Error Details**: Check verbose logs (--log-level debug)

---

Created with Python 3.10+, FastAPI, and async best practices.
