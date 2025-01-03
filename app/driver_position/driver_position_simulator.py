import math
import random
import uuid
from datetime import datetime, timedelta

import h3

from app.driver_position.schemas import DriverPosition

# Constants for Belo Horizonte coordinates
BH_LAT_MIN = -20.0047113796
BH_LAT_MAX = -19.7890619963
BH_LON_MIN = -44.0986149944
BH_LON_MAX = -43.860692326

# Constants for simulation
K_DRIVERS = 10
AVERAGE_VELOCITY = 50
MAX_DRIVE_DISTANCE = 2
TIME_STEP = 1
UPDATE_THRESHOLD = timedelta(seconds=30)


class DriverPositionSimulator:
    def __init__(
        self,
        k_drivers=K_DRIVERS,
        average_velocity=AVERAGE_VELOCITY,
        max_drive_distance=MAX_DRIVE_DISTANCE,
    ):
        self.k_drivers = k_drivers
        self.average_velocity = average_velocity
        self.max_drive_distance = max_drive_distance
        self.driver_positions = {}
        self.last_updated = {}
        self.driver_ids = [uuid.uuid4() for _ in range(k_drivers)]

    @staticmethod
    def generate_driver_position(driver_id):
        """Generate an initial random position for a driver within Belo Horizonte's coordinates."""
        latitude = random.uniform(BH_LAT_MIN, BH_LAT_MAX)
        longitude = random.uniform(BH_LON_MIN, BH_LON_MAX)
        h3_cell = h3.latlng_to_cell(latitude, longitude, 7)  # Resolution 7 H3 cell

        return DriverPosition(
            driver_id=driver_id,
            latitude=latitude,
            longitude=longitude,
            timestamp=datetime.utcnow(),
            h3_cell=h3_cell,
        )

    def new_position(self, latitude, longitude, velocity, time_delta):
        """Update the driver's position based on velocity and elapsed time."""
        angle = random.uniform(0, 2 * math.pi)

        distance_traveled = min(
            (velocity / 3600) * time_delta.total_seconds(), self.max_drive_distance
        )

        delta_lat = (distance_traveled * math.cos(angle)) / 110.574
        delta_lon = (distance_traveled * math.sin(angle)) / (
            111.32 * math.cos(math.radians(latitude))
        )

        new_latitude = latitude + delta_lat
        new_longitude = longitude + delta_lon

        return new_latitude, new_longitude

    def initialize_positions(self):
        """Initialize positions for all drivers."""
        for driver_id in self.driver_ids:
            self.driver_positions[driver_id] = self.generate_driver_position(driver_id)
            self.last_updated[driver_id] = (
                datetime.min
            )  # Initialize with a very old timestamp

    def update_position(self):
        """Update the position for a driver who hasn't been updated in the last 30 seconds."""
        now = datetime.utcnow()
        eligible_drivers = [
            driver_id
            for driver_id in self.driver_ids
            if now - self.last_updated[driver_id] > UPDATE_THRESHOLD
        ]

        if not eligible_drivers:
            return None

        driver_id = random.choice(eligible_drivers)  # Select one random eligible driver
        driver_position = self.driver_positions[driver_id]

        time_delta = now - self.last_updated[driver_id]

        new_latitude, new_longitude = self.new_position(
            driver_position.latitude,
            driver_position.longitude,
            self.average_velocity,
            time_delta,
        )

        driver_position.latitude = new_latitude
        driver_position.longitude = new_longitude
        driver_position.timestamp = now
        driver_position.h3_cell = h3.latlng_to_cell(new_latitude, new_longitude, 7)

        self.last_updated[driver_id] = now

        return driver_position

    def get_driver_positions(self):
        """Get the current positions of all drivers."""
        return list(self.driver_positions.values())
