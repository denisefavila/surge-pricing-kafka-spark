from fastapi import APIRouter, Query

from app.data_aggregator_service import REDIS_CLIENT
from app.orders.service import OrderAggregator
from app.schemas import PositionsCountResponse

router = APIRouter()


@router.get("/order_count", response_model=PositionsCountResponse)
def order_count(cell_resolution: int = Query(..., description="H3 cell resolution")):
    """API endpoint to get the real-time driver count."""

    orders_aggregator = OrderAggregator(REDIS_CLIENT)
    return orders_aggregator.get_order_count_for_all_cells(
        cell_resolution=cell_resolution
    )
