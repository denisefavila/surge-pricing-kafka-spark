from app.data_aggregator_service import DataAggregator

TIME_WINDOW_MINUTES = 5

DRIVER_COUNT_KEY = "driver_count_by_region"


class DriverPositionAggregator(DataAggregator):
    def __init__(self, redis_client, time_window_minutes=TIME_WINDOW_MINUTES):
        super().__init__(
            redis_client,
            key_prefix=DRIVER_COUNT_KEY,
            time_window_minutes=time_window_minutes,
        )

    def get_driver_count_for_all_cells(self, cell_resolution: int):
        """Fetch and return driver count for all cells."""
        return self.get_aggregated_data(cell_resolution)

    def get_driver_count_in_last_minute(self, cell_id: str):
        return self.get_count_in_last_minute(cell_id=cell_id)
