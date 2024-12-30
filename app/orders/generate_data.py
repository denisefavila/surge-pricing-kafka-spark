import random
import uuid
from datetime import datetime
from decimal import Decimal

import h3

from app.orders.schemas import Order

BH_LAT_CENTER = -19.9191
BH_LON_CENTER = -43.9386

LAT_STDDEV = 0.01
LON_STDDEV = 0.01


def generate_order():
    """Generate an order within Belo Horizonte's coordinates."""

    # Generate random data
    order_id = uuid.uuid4()
    latitude = random.gauss(BH_LAT_CENTER, LAT_STDDEV)
    longitude = random.gauss(BH_LON_CENTER, LON_STDDEV)
    h3_cell = h3.latlng_to_cell(latitude, longitude, 7)  # Resolution 7 H3 cell

    # Create the Order object using the generated data
    return Order(
        order_id=order_id,
        customer_id=uuid.uuid4(),
        order_value=Decimal(random.uniform(10.0, 500.0)),
        latitude=latitude,
        longitude=longitude,
        timestamp=datetime.utcnow(),
        h3_cell=h3_cell,
    )
