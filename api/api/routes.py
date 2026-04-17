"""
API Routes for 5G Network Slicing System.
"""

from fastapi import APIRouter, WebSocket, HTTPException, Query, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio
import numpy as np
from datetime import datetime

from schemas.traffic import (
    TrafficBatch,
    TrafficDataItem,
    PredictionResponse,
    AllocationDecision,
    SLAStatus,
)
from core.config import config


router = APIRouter()

# In-memory buffer for traffic data
traffic_buffer: List[Dict] = []
connected_clients: List[WebSocket] = []


@router.get("/health")
async def health_check() -> Dict:
    """
    Health check endpoint.

    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "version": config.API_VERSION,
        "timestamp": datetime.now().timestamp(),
    }


@router.post("/ingest")
async def ingest_traffic(batch: TrafficBatch) -> Dict:
    """
    Ingest traffic data batch.

    Args:
        batch: TrafficBatch object

    Returns:
        Ingestion confirmation
    """
    # Store traffic data
    for item in batch.data:
        traffic_buffer.append(item.model_dump())

    # Maintain buffer size limit
    if len(traffic_buffer) > config.BUFFER_SIZE:
        traffic_buffer.pop(0)

    # Broadcast to WebSocket clients
    message = {
        "type": "traffic_ingested",
        "batch_id": batch.batch_id,
        "item_count": len(batch.data),
        "timestamp": datetime.now().timestamp(),
    }

    for client in connected_clients[:]:
        try:
            await client.send_json(message)
        except Exception:
            connected_clients.remove(client)

    return {
        "status": "ingested",
        "batch_id": batch.batch_id,
        "items_received": len(batch.data),
        "buffer_size": len(traffic_buffer),
    }


@router.get("/predict/{slice_id}")
async def predict_allocation(
    slice_id: str, use_mock: bool = Query(True)
) -> PredictionResponse:
    """
    Predict resource allocation for a slice.

    Args:
        slice_id: Slice identifier
        use_mock: Use mock predictions if True

    Returns:
        Prediction response with allocation decision
    """
    # Verify slice exists
    slice_config = config.get_slice(slice_id)
    if not slice_config:
        raise HTTPException(status_code=404, detail=f"Slice {slice_id} not found")

    # Generate mock prediction
    allocated_bw = np.random.uniform(
        slice_config.max_bandwidth * 0.3, slice_config.max_bandwidth * 0.8
    )
    priority = slice_config.priority

    # Simulate latency (random for mock)
    simulated_latency = np.random.uniform(1, 100)
    simulated_throughput = np.random.uniform(
        slice_config.min_throughput * 0.8, slice_config.min_throughput * 1.2
    )

    decision = AllocationDecision(
        slice_id=slice_id,
        allocated_bandwidth=round(allocated_bw, 2),
        priority_level=priority,
        action_id=f"action_{datetime.now().timestamp()}",
        confidence=round(np.random.uniform(0.75, 0.99), 4),
    )

    sla_status = SLAStatus(
        slice_id=slice_id,
        is_compliant=simulated_latency <= slice_config.min_latency_threshold and simulated_throughput >= slice_config.min_throughput,
        latency_ms=round(simulated_latency, 2),
        throughput_mbps=round(simulated_throughput, 2),
        violation_reason=None if simulated_latency <= slice_config.min_latency_threshold else "Latency exceeded",
    )

    return PredictionResponse(
        slice_id=slice_id,
        decision=decision,
        sla_status=sla_status,
        timestamp=datetime.now().timestamp(),
    )


@router.get("/slices")
async def list_slices() -> Dict:
    """
    List all configured slices.

    Returns:
        List of slice configurations
    """
    slices = []
    for slice_id, slice_config in config.SLICES.items():
        slices.append(
            {
                "slice_id": slice_config.slice_id,
                "slice_type": slice_config.slice_type,
                "max_bandwidth": slice_config.max_bandwidth,
                "min_latency_threshold": slice_config.min_latency_threshold,
                "min_throughput": slice_config.min_throughput,
                "priority": slice_config.priority,
            }
        )

    return {"slices": slices, "total": len(slices)}


@router.get("/traffic/statistics")
async def get_traffic_statistics() -> Dict:
    """
    Get statistics on ingested traffic.

    Returns:
        Traffic statistics
    """
    if not traffic_buffer:
        return {
            "total_items": 0,
            "avg_bandwidth_demand": 0.0,
            "message": "No traffic data available",
        }

    bandwidth_demands = [item.get("bandwidth_demand", 0) for item in traffic_buffer]
    latency_reqs = [item.get("latency_requirement", 0) for item in traffic_buffer]

    return {
        "total_items": len(traffic_buffer),
        "avg_bandwidth_demand": round(np.mean(bandwidth_demands), 2),
        "max_bandwidth_demand": round(np.max(bandwidth_demands), 2),
        "avg_latency_requirement": round(np.mean(latency_reqs), 2),
        "latest_timestamp": max(
            (item.get("timestamp", 0) for item in traffic_buffer), default=0
        ),
    }


@router.get("/traffic/buffer")
async def get_traffic_buffer(limit: int = Query(10)) -> Dict:
    """
    Retrieve traffic buffer (most recent items).

    Args:
        limit: Number of recent items to return

    Returns:
        Recent traffic data
    """
    recent_items = traffic_buffer[-limit:] if traffic_buffer else []

    return {
        "buffer_size": len(traffic_buffer),
        "items_returned": len(recent_items),
        "data": recent_items,
    }


@router.websocket("/stream")
async def websocket_stream(websocket: WebSocket) -> None:
    """
    WebSocket endpoint for streaming traffic data.

    Args:
        websocket: WebSocket connection
    """
    await websocket.accept()
    connected_clients.append(websocket)

    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()

            if data == "ping":
                await websocket.send_json({"type": "pong", "timestamp": datetime.now().timestamp()})
            elif data == "stats":
                # Send current statistics
                await websocket.send_json(
                    {
                        "type": "statistics",
                        "buffer_size": len(traffic_buffer),
                        "timestamp": datetime.now().timestamp(),
                    }
                )
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
    except Exception as e:
        if websocket in connected_clients:
            connected_clients.remove(websocket)


@router.post("/clear-buffer")
async def clear_traffic_buffer() -> Dict:
    """
    Clear the in-memory traffic buffer.

    Returns:
        Confirmation
    """
    global traffic_buffer
    cleared_count = len(traffic_buffer)
    traffic_buffer.clear()

    return {
        "status": "buffer_cleared",
        "items_cleared": cleared_count,
        "timestamp": datetime.now().timestamp(),
    }
