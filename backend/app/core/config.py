"""
Core configuration for the 5G Network Slicing System.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SliceConfig:
    """Configuration for network slices."""

    slice_id: str
    slice_type: str  # "eMBB", "URLLC", "mMTC"
    max_bandwidth: float  # in Mbps
    min_latency_threshold: float  # in ms
    min_throughput: float  # in Mbps
    priority: int


class AppConfig:
    """Application-wide configuration."""

    DEBUG: bool = True
    API_TITLE: str = "5G Network Slicing System"
    API_VERSION: str = "0.1.0"

    # Slice configurations
    SLICES: Dict[str, SliceConfig] = {
        "slice_embb": SliceConfig(
            slice_id="slice_embb",
            slice_type="eMBB",
            max_bandwidth=1000.0,
            min_latency_threshold=50.0,
            min_throughput=100.0,
            priority=2,
        ),
        "slice_urllc": SliceConfig(
            slice_id="slice_urllc",
            slice_type="URLLC",
            max_bandwidth=500.0,
            min_latency_threshold=1.0,
            min_throughput=50.0,
            priority=1,
        ),
        "slice_mmtc": SliceConfig(
            slice_id="slice_mmtc",
            slice_type="mMTC",
            max_bandwidth=200.0,
            min_latency_threshold=100.0,
            min_throughput=20.0,
            priority=3,
        ),
    }

    # System parameters
    BUFFER_SIZE: int = 1000
    ALLOCATION_UPDATE_INTERVAL: float = 1.0  # seconds

    @classmethod
    def get_slice(cls, slice_id: str) -> SliceConfig:
        """Get slice configuration by ID."""
        return cls.SLICES.get(slice_id)


config = AppConfig()
