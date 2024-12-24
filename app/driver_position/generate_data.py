import random
import uuid
from datetime import datetime

import h3

BH_LAT_MIN = -20.0047113796
BH_LAT_MAX = -19.7890619963
BH_LON_MIN = -44.0986149944
BH_LON_MAX = -43.860692326


def generate_driver_position():
    """Generate a driver's position within Belo Horizonte's coordinates."""
    driver_id = uuid.uuid4()
    latitude = random.uniform(BH_LAT_MIN, BH_LAT_MAX)
    longitude = random.uniform(BH_LON_MIN, BH_LON_MAX)
    h3_cell = h3.latlng_to_cell(latitude, longitude, 7)  # Resolution 7 H3 cell

    return {
        "driver_id": str(driver_id),
        "latitude": f"{latitude:.6f}",
        "longitude": f"{longitude:.6f}",
        "timestamp": datetime.utcnow().isoformat(),
        "h3_cell": h3_cell,
    }
