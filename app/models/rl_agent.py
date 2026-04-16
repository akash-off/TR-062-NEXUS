"""
Mock Reinforcement Learning Agent for network slice allocation.
This is a prototype implementation - no actual training occurs.
"""

import random
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class AgentState:
    """State representation for the RL agent."""

    slice_id: str
    current_bandwidth: float
    latency_requirement: float
    packet_count: int
    priority: int
    timestamp: float
    normalized_bandwidth: float = 0.0
    normalized_latency: float = 0.0


class MockRLAgent:
    """
    Mock RL Agent for allocation decisions.
    Uses rule-based logic instead of actual ML training.
    """

    def __init__(self, max_bandwidth: float = 2000.0):
        """
        Initialize the mock RL agent.

        Args:
            max_bandwidth: Maximum total bandwidth available in Mbps
        """
        self.max_bandwidth = max_bandwidth
        self.action_history: List[Dict] = []
        self.state_history: List[AgentState] = []
        self.action_counter = 0

    def normalize_state(self, state: AgentState) -> AgentState:
        """
        Normalize state values to 0-1 range.

        Args:
            state: Raw state from traffic data

        Returns:
            Normalized state
        """
        # Normalize bandwidth to [0, 1]
        state.normalized_bandwidth = min(state.current_bandwidth / self.max_bandwidth, 1.0)

        # Normalize latency to [0, 1] (assume max latency 1000ms)
        state.normalized_latency = min(state.latency_requirement / 1000.0, 1.0)

        return state

    def compute_allocation(self, state: AgentState) -> Tuple[float, int]:
        """
        Rule-based allocation logic (mock RL).

        Allocation strategy:
        - URLLC (priority 1): High bandwidth, minimal latency
        - eMBB (priority 2): Variable bandwidth, normal latency
        - mMTC (priority 3): Low bandwidth, flexible latency

        Args:
            state: Normalized agent state

        Returns:
            Tuple of (allocated_bandwidth, priority_level)
        """
        # Normalize the state
        state = self.normalize_state(state)

        # Rule-based decision making
        if state.priority == 1:  # URLLC
            allocated_bandwidth = min(
                state.current_bandwidth + 100, self.max_bandwidth * 0.3
            )
            priority_level = 1
        elif state.priority == 2:  # eMBB
            allocated_bandwidth = min(
                state.current_bandwidth * 1.2, self.max_bandwidth * 0.5
            )
            priority_level = 2
        else:  # mMTC (priority 3)
            allocated_bandwidth = min(
                state.current_bandwidth * 0.8, self.max_bandwidth * 0.2
            )
            priority_level = 3

        # Add small random noise for realism
        allocated_bandwidth += random.uniform(-5, 5)
        allocated_bandwidth = max(allocated_bandwidth, 10.0)  # Minimum 10 Mbps

        return allocated_bandwidth, priority_level

    def get_action(self, state: AgentState) -> Dict:
        """
        Get allocation action from state (mock RL inference).

        Args:
            state: Current state

        Returns:
            Dictionary with allocation decision
        """
        self.state_history.append(state)

        # Compute allocation
        allocated_bandwidth, priority_level = self.compute_allocation(state)

        # Generate action ID
        self.action_counter += 1
        action_id = f"action_{self.action_counter:06d}"

        # Mock confidence score (higher for URLLC, lower for mMTC)
        base_confidence = {"1": 0.95, "2": 0.85, "3": 0.75}.get(
            str(state.priority), 0.80
        )
        confidence = base_confidence + random.uniform(-0.05, 0.05)
        confidence = max(0.0, min(1.0, confidence))  # Clamp to [0, 1]

        action = {
            "action_id": action_id,
            "allocated_bandwidth": round(allocated_bandwidth, 2),
            "priority_level": priority_level,
            "confidence": round(confidence, 4),
            "timestamp": datetime.now().timestamp(),
        }

        self.action_history.append(action)

        return action

    def get_state_from_traffic(
        self, traffic_data: Dict, slice_id: str, priority: int
    ) -> AgentState:
        """
        Convert traffic data to agent state.

        Args:
            traffic_data: Raw traffic data dictionary
            slice_id: Slice identifier
            priority: Priority level

        Returns:
            AgentState object
        """
        state = AgentState(
            slice_id=slice_id,
            current_bandwidth=traffic_data.get("bandwidth_demand", 50.0),
            latency_requirement=traffic_data.get("latency_requirement", 10.0),
            packet_count=traffic_data.get("packet_count", 100),
            priority=priority,
            timestamp=traffic_data.get("timestamp", datetime.now().timestamp()),
        )

        return state

    def reset(self) -> None:
        """Reset agent state history and action counter."""
        self.state_history.clear()
        self.action_history.clear()
        self.action_counter = 0

    def get_statistics(self) -> Dict:
        """
        Get agent statistics.

        Returns:
            Dictionary with agent stats
        """
        if not self.action_history:
            return {"total_actions": 0, "avg_allocation": 0.0}

        allocations = [a["allocated_bandwidth"] for a in self.action_history]

        return {
            "total_actions": len(self.action_history),
            "avg_allocation": round(np.mean(allocations), 2),
            "min_allocation": round(np.min(allocations), 2),
            "max_allocation": round(np.max(allocations), 2),
        }
