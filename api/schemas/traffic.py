"""
Pydantic models for traffic data and API responses.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class SliceType(str, Enum):
    """Network slice types."""

    EMBB = "eMBB"
    URLLC = "URLLC"
    MMTC = "mMTC"


class TrafficDataItem(BaseModel):
    """Single traffic data point."""

    timestamp: float = Field(..., description="Unix timestamp")
    slice_id: str = Field(..., description="Slice identifier")
    slice_type: SliceType = Field(..., description="Type of slice")
    bandwidth_demand: float = Field(..., description="Bandwidth demand in Mbps")
    latency_requirement: float = Field(..., description="Latency requirement in ms")
    packet_count: int = Field(..., description="Number of packets")
    priority: int = Field(..., description="User priority (1-5, 1=highest)")


class TrafficBatch(BaseModel):
    """Batch of traffic data."""

    batch_id: str = Field(..., description="Batch identifier")
    data: List[TrafficDataItem] = Field(..., description="List of traffic items")
    timestamp: float = Field(..., description="Batch creation timestamp")


class AllocationDecision(BaseModel):
    """RL agent allocation decision."""

    slice_id: str = Field(..., description="Target slice")
    allocated_bandwidth: float = Field(..., description="Allocated bandwidth in Mbps")
    priority_level: int = Field(..., description="Priority level (1-5)")
    action_id: str = Field(..., description="Unique action identifier")
    confidence: float = Field(..., description="Confidence score (0.0-1.0)")


class SLAStatus(BaseModel):
    """SLA compliance status."""

    slice_id: str = Field(..., description="Slice identifier")
    is_compliant: bool = Field(..., description="SLA compliance status")
    latency_ms: float = Field(..., description="Observed latency in ms")
    throughput_mbps: float = Field(..., description="Observed throughput in Mbps")
    violation_reason: Optional[str] = Field(
        None, description="Reason if not compliant"
    )


class PredictionResponse(BaseModel):
    """Response from prediction endpoint."""

    slice_id: str = Field(..., description="Slice identifier")
    decision: AllocationDecision = Field(..., description="Allocation decision")
    sla_status: SLAStatus = Field(..., description="SLA status")
    timestamp: float = Field(..., description="Response timestamp")


class HealthCheck(BaseModel):
    """Health check response."""

    status: str = Field(..., description="System status")
    version: str = Field(..., description="API version")
    uptime_seconds: float = Field(..., description="Uptime in seconds")
