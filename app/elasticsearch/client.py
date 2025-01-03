import logging
from datetime import datetime
from logging import Handler

from elasticsearch import Elasticsearch


class ElasticsearchHandler(Handler):
    def __init__(self, es_client, index_name):
        super().__init__()
        self.es_client = es_client
        self.index_name = index_name

    def emit(self, record):
        log_entry = self.format(record)
        structured_data = getattr(record, "structured_data", {})
        document = {
            "message": record.msg,
            "level": record.levelname,
            "timestamp": datetime.utcnow().isoformat(),
            **structured_data,  # Merge structured data into the document
        }
        self.es_client.index(index=self.index_name, document=document)


# Configure Elasticsearch logging
es = Elasticsearch([{"host": "localhost", "port": 9200}])
es_handler = ElasticsearchHandler(es, "driver_position_logs")

logger = logging.getLogger("elasticsearch_logger")
logger.setLevel(logging.INFO)
logger.addHandler(es_handler)

# Log structured data
logger.info("Driver position update", extra={"structured_data": position.to_dict()})
