import logging
import os
import random
import signal
import time
import uuid
from contextlib import contextmanager
from datetime import datetime

import redis

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@contextmanager
def redis_client(redis_host, redis_port):
    """Context manager for Redis client."""
    client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    try:
        logger.info(f"Connecting to Redis at {redis_host}:{redis_port}")
        yield client
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {e}")
        raise
    finally:
        logger.info("Closing Redis connection.")
        client.close()
