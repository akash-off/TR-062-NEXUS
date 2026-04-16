"""
Traffic Simulator for 5G Network Slicing System.
Generates synthetic 5G traffic patterns.
"""

import random
import httpx
import asyncio
import numpy as np
from datetime import datetime
from enum import Enum
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class TrafficPattern(str, Enum):
    """Traffic pattern types."""

    RANDOM = "random"
    BURST = "burst"
    STEADY = "steady"


class TrafficSimulator:
    """
    Simulates synthetic 5G traffic for different slice types.
    """

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        """
        Initialize traffic simulator.

        Args:
            api_base_url: Base URL of the API
        """
        self.api_base_url = api_base_url
        self.ingest_endpoint = f"{api_base_url}/api/ingest"
        self.batch_counter = 0
        self.item_counter = 0

    async def generate_embb_traffic(
        self, pattern: TrafficPattern = TrafficPattern.RANDOM
    ) -> Dict:
        """
        Generate eMBB (Enhanced Mobile Broadband) traffic.

        Args:
            pattern: Traffic pattern type

        Returns:
            Traffic data item
        """
        if pattern == TrafficPattern.BURST:
            bandwidth_demand = np.random.uniform(800, 1000)
            latency_req = np.random.uniform(20, 50)
        elif pattern == TrafficPattern.STEADY:
            bandwidth_demand = np.random.uniform(500, 700)
            latency_req = np.random.uniform(30, 60)
        else:  # RANDOM
            bandwidth_demand = np.random.uniform(100, 1000)
            latency_req = np.random.uniform(10, 100)

        return {
            "timestamp": datetime.now().timestamp(),
            "slice_id": "slice_embb",
            "slice_type": "eMBB",
            "bandwidth_demand": round(bandwidth_demand, 2),
            "latency_requirement": round(latency_req, 2),
            "packet_count": random.randint(100, 10000),
            "priority": 2,
        }

    async def generate_urllc_traffic(
        self, pattern: TrafficPattern = TrafficPattern.RANDOM
    ) -> Dict:
        """
        Generate URLLC (Ultra-Reliable Low-Latency) traffic.

        Args:
            pattern: Traffic pattern type

        Returns:
            Traffic data item
        """
        if pattern == TrafficPattern.BURST:
            bandwidth_demand = np.random.uniform(300, 500)
            latency_req = np.random.uniform(0.5, 2.0)
        elif pattern == TrafficPattern.STEADY:
            bandwidth_demand = np.random.uniform(200, 350)
            latency_req = np.random.uniform(0.5, 1.5)
        else:  # RANDOM
            bandwidth_demand = np.random.uniform(50, 500)
            latency_req = np.random.uniform(0.1, 5.0)

        return {
            "timestamp": datetime.now().timestamp(),
            "slice_id": "slice_urllc",
            "slice_type": "URLLC",
            "bandwidth_demand": round(bandwidth_demand, 2),
            "latency_requirement": round(latency_req, 2),
            "packet_count": random.randint(50, 1000),
            "priority": 1,
        }

    async def generate_mmtc_traffic(
        self, pattern: TrafficPattern = TrafficPattern.RANDOM
    ) -> Dict:
        """
        Generate mMTC (Massive IoT) traffic.

        Args:
            pattern: Traffic pattern type

        Returns:
            Traffic data item
        """
        if pattern == TrafficPattern.BURST:
            bandwidth_demand = np.random.uniform(150, 250)
            latency_req = np.random.uniform(500, 1000)
        elif pattern == TrafficPattern.STEADY:
            bandwidth_demand = np.random.uniform(80, 150)
            latency_req = np.random.uniform(500, 800)
        else:  # RANDOM
            bandwidth_demand = np.random.uniform(10, 200)
            latency_req = np.random.uniform(100, 1000)

        return {
            "timestamp": datetime.now().timestamp(),
            "slice_id": "slice_mmtc",
            "slice_type": "mMTC",
            "bandwidth_demand": round(bandwidth_demand, 2),
            "latency_requirement": round(latency_req, 2),
            "packet_count": random.randint(1000, 50000),
            "priority": 3,
        }

    async def generate_traffic_batch(
        self, batch_size: int = 10, pattern: TrafficPattern = TrafficPattern.RANDOM
    ) -> List[Dict]:
        """
        Generate a batch of mixed traffic.

        Args:
            batch_size: Number of items in batch
            pattern: Traffic pattern type

        Returns:
            List of traffic data items
        """
        batch = []

        for _ in range(batch_size):
            # Randomly select slice type
            slice_type = random.choice([1, 2, 3])

            if slice_type == 1:
                traffic = await self.generate_urllc_traffic(pattern)
            elif slice_type == 2:
                traffic = await self.generate_embb_traffic(pattern)
            else:
                traffic = await self.generate_mmtc_traffic(pattern)

            batch.append(traffic)
            self.item_counter += 1

        return batch

    async def send_batch_to_api(self, batch: List[Dict]) -> bool:
        """
        Send traffic batch to API.

        Args:
            batch: List of traffic items

        Returns:
            Success status
        """
        if not batch:
            return False

        self.batch_counter += 1
        batch_id = f"batch_{self.batch_counter:06d}"

        payload = {
            "batch_id": batch_id,
            "data": batch,
            "timestamp": datetime.now().timestamp(),
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(self.ingest_endpoint, json=payload)
                if response.status_code == 200:
                    logger.info(f"Batch {batch_id} sent successfully ({len(batch)} items)")
                    return True
                else:
                    logger.error(f"Failed to send batch: {response.status_code}")
                    return False
        except Exception as e:
            logger.error(f"Error sending batch: {e}")
            return False

    async def simulate_continuous(
        self,
        duration_seconds: int = 60,
        batch_interval_seconds: float = 1.0,
        batch_size: int = 10,
        pattern: TrafficPattern = TrafficPattern.RANDOM,
    ) -> None:
        """
        Run continuous traffic simulation.

        Args:
            duration_seconds: Duration of simulation
            batch_interval_seconds: Interval between batches
            batch_size: Number of items per batch
            pattern: Traffic pattern type
        """
        logger.info(
            f"Starting simulation for {duration_seconds}s "
            f"(batch every {batch_interval_seconds}s, {batch_size} items/batch)"
        )

        elapsed = 0

        while elapsed < duration_seconds:
            try:
                # Generate batch
                batch = await self.generate_traffic_batch(batch_size, pattern)

                # Send to API
                success = await self.send_batch_to_api(batch)

                if success:
                    logger.info(f"Total items sent: {self.item_counter}")

                # Wait before next batch
                await asyncio.sleep(batch_interval_seconds)
                elapsed += batch_interval_seconds

            except Exception as e:
                logger.error(f"Simulation error: {e}")
                await asyncio.sleep(1)

        logger.info(
            f"Simulation complete. Batches: {self.batch_counter}, Items: {self.item_counter}"
        )

    async def test_api_connectivity(self) -> bool:
        """
        Test connectivity to the API.

        Returns:
            True if connected
        """
        try:
            health_url = f"{self.api_base_url}/health"
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(health_url)
                if response.status_code == 200:
                    logger.info("API is reachable")
                    return True
        except Exception as e:
            logger.error(f"Cannot reach API: {e}")

        return False


async def main():
    """Main entry point for simulator."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    simulator = TrafficSimulator()

    # Test connectivity
    if not await simulator.test_api_connectivity():
        logger.error("Cannot connect to API. Make sure it's running on http://localhost:8000")
        return

    # Run simulation
    await simulator.simulate_continuous(
        duration_seconds=120,
        batch_interval_seconds=1.0,
        batch_size=10,
        pattern=TrafficPattern.RANDOM,
    )


if __name__ == "__main__":
    asyncio.run(main())
