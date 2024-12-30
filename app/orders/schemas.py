import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Order:
    order_id: uuid.UUID
    customer_id: uuid.UUID
    order_value: Decimal
    latitude: float
    longitude: float
    timestamp: datetime
    h3_cell: str

    def to_dict(self):
        return {
            "order_id": str(self.order_id),
            "customer_id": str(self.customer_id),
            "order_value": float(self.order_value),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.isoformat(),
            "h3_cell": self.h3_cell,
        }
