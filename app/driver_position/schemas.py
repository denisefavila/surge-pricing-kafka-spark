import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DriverPosition:
    driver_id: uuid.UUID
    latitude: float
    longitude: float
    timestamp: datetime
    h3_cell: str

    def to_dict(self):
        return {
            "driver_id": str(self.driver_id),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.isoformat(),
            "h3_cell": self.h3_cell,
        }
