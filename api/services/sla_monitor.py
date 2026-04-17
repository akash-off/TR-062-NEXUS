"""
SLA (Service Level Agreement) Monitoring Service.
Validates compliance with latency and throughput requirements.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import numpy as np


@dataclass
class SLAViolation:
    """Record of SLA violation."""

    slice_id: str
    violation_type: str  # "latency" or "throughput"
    threshold: float
    actual_value: float
    timestamp: float
    severity: str  # "warning" or "critical"


@dataclass
class SLAMetrics:
    """SLA metrics for a slice."""

    slice_id: str
    required_latency_ms: float
    minimum_throughput_mbps: float
    observed_latency_ms: float = 0.0
    observed_throughput_mbps: float = 0.0
    is_compliant: bool = True
    violations: List[SLAViolation] = field(default_factory=list)
    last_check_time: float = 0.0


class SLAMonitor:
    """
    Monitors SLA compliance for network slices.
    """

    def __init__(self):
        """Initialize SLA monitor."""
        self.slice_metrics: Dict[str, SLAMetrics] = {}
        self.violation_history: List[SLAViolation] = []
        self.check_interval_seconds = 1.0

    def register_slice(
        self, slice_id: str, latency_sla_ms: float, throughput_sla_mbps: float
    ) -> None:
        """
        Register a slice for SLA monitoring.

        Args:
            slice_id: Slice identifier
            latency_sla_ms: Latency SLA requirement in ms
            throughput_sla_mbps: Throughput SLA requirement in Mbps
        """
        self.slice_metrics[slice_id] = SLAMetrics(
            slice_id=slice_id,
            required_latency_ms=latency_sla_ms,
            minimum_throughput_mbps=throughput_sla_mbps,
        )

    def check_latency_compliance(
        self, slice_id: str, observed_latency_ms: float
    ) -> Tuple[bool, str]:
        """
        Check if latency is within SLA.

        Args:
            slice_id: Slice identifier
            observed_latency_ms: Observed latency in ms

        Returns:
            Tuple of (is_compliant: bool, reason: str)
        """
        if slice_id not in self.slice_metrics:
            return False, "Slice not registered"

        metrics = self.slice_metrics[slice_id]
        metrics.observed_latency_ms = observed_latency_ms

        is_compliant = observed_latency_ms <= metrics.required_latency_ms

        if not is_compliant:
            violation = SLAViolation(
                slice_id=slice_id,
                violation_type="latency",
                threshold=metrics.required_latency_ms,
                actual_value=observed_latency_ms,
                timestamp=datetime.now().timestamp(),
                severity="critical" if observed_latency_ms > metrics.required_latency_ms * 1.5 else "warning",
            )
            self.violation_history.append(violation)
            metrics.violations.append(violation)

        return is_compliant, "Latency within SLA" if is_compliant else "Latency exceeded SLA"

    def check_throughput_compliance(
        self, slice_id: str, observed_throughput_mbps: float
    ) -> Tuple[bool, str]:
        """
        Check if throughput is within SLA.

        Args:
            slice_id: Slice identifier
            observed_throughput_mbps: Observed throughput in Mbps

        Returns:
            Tuple of (is_compliant: bool, reason: str)
        """
        if slice_id not in self.slice_metrics:
            return False, "Slice not registered"

        metrics = self.slice_metrics[slice_id]
        metrics.observed_throughput_mbps = observed_throughput_mbps

        is_compliant = observed_throughput_mbps >= metrics.minimum_throughput_mbps

        if not is_compliant:
            violation = SLAViolation(
                slice_id=slice_id,
                violation_type="throughput",
                threshold=metrics.minimum_throughput_mbps,
                actual_value=observed_throughput_mbps,
                timestamp=datetime.now().timestamp(),
                severity="critical",
            )
            self.violation_history.append(violation)
            metrics.violations.append(violation)

        return is_compliant, "Throughput within SLA" if is_compliant else "Throughput below SLA"

    def validate_slice_sla(
        self, slice_id: str, latency_ms: float, throughput_mbps: float
    ) -> Dict:
        """
        Perform full SLA validation for a slice.

        Args:
            slice_id: Slice identifier
            latency_ms: Observed latency in ms
            throughput_mbps: Observed throughput in Mbps

        Returns:
            Dictionary with compliance status
        """
        latency_ok, latency_reason = self.check_latency_compliance(slice_id, latency_ms)
        throughput_ok, throughput_reason = self.check_throughput_compliance(
            slice_id, throughput_mbps
        )

        overall_compliant = latency_ok and throughput_ok

        if slice_id in self.slice_metrics:
            self.slice_metrics[slice_id].is_compliant = overall_compliant
            self.slice_metrics[slice_id].last_check_time = datetime.now().timestamp()

        return {
            "slice_id": slice_id,
            "is_compliant": overall_compliant,
            "latency_compliant": latency_ok,
            "latency_reason": latency_reason,
            "throughput_compliant": throughput_ok,
            "throughput_reason": throughput_reason,
            "observed_latency_ms": latency_ms,
            "observed_throughput_mbps": throughput_mbps,
            "timestamp": datetime.now().timestamp(),
        }

    def get_slice_status(self, slice_id: str) -> Dict:
        """
        Get current SLA status for a slice.

        Args:
            slice_id: Slice identifier

        Returns:
            Dictionary with SLA status
        """
        if slice_id not in self.slice_metrics:
            return {"error": "Slice not found"}

        metrics = self.slice_metrics[slice_id]

        return {
            "slice_id": slice_id,
            "is_compliant": metrics.is_compliant,
            "required_latency_ms": metrics.required_latency_ms,
            "observed_latency_ms": round(metrics.observed_latency_ms, 2),
            "minimum_throughput_mbps": metrics.minimum_throughput_mbps,
            "observed_throughput_mbps": round(metrics.observed_throughput_mbps, 2),
            "violation_count": len(metrics.violations),
        }

    def get_violation_statistics(self) -> Dict:
        """
        Get violation statistics.

        Returns:
            Dictionary with violation stats
        """
        if not self.violation_history:
            return {
                "total_violations": 0,
                "latency_violations": 0,
                "throughput_violations": 0,
                "critical_violations": 0,
            }

        latency_violations = sum(
            1 for v in self.violation_history if v.violation_type == "latency"
        )
        throughput_violations = sum(
            1 for v in self.violation_history if v.violation_type == "throughput"
        )
        critical_violations = sum(
            1 for v in self.violation_history if v.severity == "critical"
        )

        return {
            "total_violations": len(self.violation_history),
            "latency_violations": latency_violations,
            "throughput_violations": throughput_violations,
            "critical_violations": critical_violations,
        }

    def clear_old_violations(self, max_age_seconds: float = 3600.0) -> int:
        """
        Remove violations older than max_age_seconds.

        Args:
            max_age_seconds: Maximum age in seconds

        Returns:
            Number of violations cleared
        """
        current_time = datetime.now().timestamp()
        cleared_count = 0

        for violation in self.violation_history[:]:
            age = current_time - violation.timestamp
            if age > max_age_seconds:
                self.violation_history.remove(violation)
                cleared_count += 1

        return cleared_count

    def reset(self) -> None:
        """Reset monitor to initial state."""
        self.slice_metrics.clear()
        self.violation_history.clear()
