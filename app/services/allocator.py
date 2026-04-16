"""
Resource Allocator Service for 5G network slices.
Manages bandwidth allocation and priority handling.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np


@dataclass
class ResourceAllocation:
    """Resource allocation record."""

    slice_id: str
    bandwidth_allocated: float
    priority_level: int
    timestamp: float
    allocation_id: str


@dataclass
class ResourceState:
    """Current resource state."""

    total_bandwidth_available: float
    bandwidth_used: float = 0.0
    allocations: List[ResourceAllocation] = field(default_factory=list)
    allocation_history: List[Dict] = field(default_factory=list)

    @property
    def bandwidth_remaining(self) -> float:
        """Calculate remaining bandwidth."""
        return self.total_bandwidth_available - self.bandwidth_used


class ResourceAllocator:
    """
    Manages network resource allocation across slices.
    """

    def __init__(self, total_bandwidth: float = 2000.0):
        """
        Initialize the resource allocator.

        Args:
            total_bandwidth: Total bandwidth available in Mbps
        """
        self.total_bandwidth = total_bandwidth
        self.state = ResourceState(total_bandwidth_available=total_bandwidth)
        self.slice_allocations: Dict[str, List[ResourceAllocation]] = {}
        self.priority_weights = {1: 1.0, 2: 0.7, 3: 0.4}  # Priority multipliers
        self.allocation_counter = 0

    def allocate_bandwidth(
        self, slice_id: str, requested_bandwidth: float, priority_level: int
    ) -> Tuple[bool, ResourceAllocation]:
        """
        Allocate bandwidth to a slice with priority handling.

        Args:
            slice_id: Target slice identifier
            requested_bandwidth: Requested bandwidth in Mbps
            priority_level: Priority level (1=highest, 5=lowest)

        Returns:
            Tuple of (success: bool, allocation: ResourceAllocation)
        """
        # Apply priority weight
        priority_weight = self.priority_weights.get(priority_level, 0.5)
        effective_request = requested_bandwidth * priority_weight

        # Check if allocation is possible
        if self.state.bandwidth_remaining < effective_request:
            # Attempt to find available bandwidth
            available = self.state.bandwidth_remaining
            if available > 10.0:  # Minimum viable allocation
                allocated = min(available, requested_bandwidth)
            else:
                return False, None
        else:
            allocated = effective_request

        # Create allocation record
        self.allocation_counter += 1
        allocation_id = f"alloc_{self.allocation_counter:06d}"

        allocation = ResourceAllocation(
            slice_id=slice_id,
            bandwidth_allocated=round(allocated, 2),
            priority_level=priority_level,
            timestamp=datetime.now().timestamp(),
            allocation_id=allocation_id,
        )

        # Update state
        self.state.bandwidth_used += allocated
        self.state.allocations.append(allocation)

        # Track per-slice allocations
        if slice_id not in self.slice_allocations:
            self.slice_allocations[slice_id] = []
        self.slice_allocations[slice_id].append(allocation)

        # Record in history
        self.state.allocation_history.append(
            {
                "allocation_id": allocation_id,
                "slice_id": slice_id,
                "bandwidth": allocated,
                "priority": priority_level,
                "timestamp": allocation.timestamp,
            }
        )

        return True, allocation

    def deallocate_bandwidth(self, allocation_id: str) -> bool:
        """
        Release allocated bandwidth.

        Args:
            allocation_id: ID of allocation to release

        Returns:
            Success status
        """
        for allocation in self.state.allocations[:]:
            if allocation.allocation_id == allocation_id:
                self.state.bandwidth_used -= allocation.bandwidth_allocated
                self.state.allocations.remove(allocation)
                return True

        return False

    def rebalance_allocations(self, slice_demands: Dict[str, float]) -> Dict[str, float]:
        """
        Rebalance bandwidth across slices based on demands.

        Args:
            slice_demands: Dictionary mapping slice_id to demand in Mbps

        Returns:
            Dictionary mapping slice_id to allocated bandwidth
        """
        if not slice_demands:
            return {}

        # Calculate total demand
        total_demand = sum(slice_demands.values())

        # If total demand exceeds capacity, proportionally reduce
        if total_demand > self.total_bandwidth:
            scale_factor = self.total_bandwidth / total_demand
            allocations = {sid: demand * scale_factor for sid, demand in slice_demands.items()}
        else:
            allocations = slice_demands.copy()

        return {k: round(v, 2) for k, v in allocations.items()}

    def get_slice_allocation(self, slice_id: str) -> float:
        """
        Get current allocated bandwidth for a slice.

        Args:
            slice_id: Slice identifier

        Returns:
            Allocated bandwidth in Mbps
        """
        if slice_id in self.slice_allocations:
            return sum(
                alloc.bandwidth_allocated
                for alloc in self.slice_allocations[slice_id]
            )
        return 0.0

    def get_state_snapshot(self) -> Dict:
        """
        Get current resource state snapshot.

        Returns:
            Dictionary with resource state
        """
        return {
            "total_bandwidth": self.total_bandwidth,
            "bandwidth_used": round(self.state.bandwidth_used, 2),
            "bandwidth_remaining": round(self.state.bandwidth_remaining, 2),
            "utilization_percent": round(
                (self.state.bandwidth_used / self.total_bandwidth) * 100, 2
            ),
            "active_allocations": len(self.state.allocations),
        }

    def clear_old_allocations(self, max_age_seconds: float = 3600.0) -> int:
        """
        Remove allocations older than max_age_seconds.

        Args:
            max_age_seconds: Maximum age in seconds

        Returns:
            Number of allocations cleared
        """
        current_time = datetime.now().timestamp()
        cleared_count = 0
        cleared_bandwidth = 0.0

        for allocation in self.state.allocations[:]:
            age = current_time - allocation.timestamp
            if age > max_age_seconds:
                cleared_bandwidth += allocation.bandwidth_allocated
                self.state.allocations.remove(allocation)
                cleared_count += 1

        self.state.bandwidth_used = max(0.0, self.state.bandwidth_used - cleared_bandwidth)

        return cleared_count

    def reset(self) -> None:
        """Reset allocator to initial state."""
        self.state = ResourceState(total_bandwidth_available=self.total_bandwidth)
        self.slice_allocations.clear()
        self.allocation_counter = 0
