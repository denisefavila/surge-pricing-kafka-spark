import random
import uuid
from datetime import datetime

import h3

BH_LAT_CENTER = -19.9191
BH_LON_CENTER = -43.9386

LAT_STDDEV = 0.01
LON_STDDEV = 0.01


def generate_order():
    order_id = uuid.uuid4()
    """Generate a order within Belo Horizonte's coordinates."""

    latitude = random.gauss(BH_LAT_CENTER, LAT_STDDEV)
    longitude = random.gauss(BH_LON_CENTER, LON_STDDEV)
    h3_cell = h3.latlng_to_cell(latitude, longitude, 7)  # Resolution 7 H3 cell
    return {
        "order_id": str(order_id),
        "customer_id": str(uuid.uuid4()),
        "order_value": f"{random.uniform(10.0, 500.0):.2f}",
        "latitude": f"{latitude:.6f}",
        "longitude": f"{random.gauss(BH_LON_CENTER, LON_STDDEV):.6f}",
        "timestamp": datetime.utcnow().isoformat(),
        "h3_cell": h3_cell,
    }
