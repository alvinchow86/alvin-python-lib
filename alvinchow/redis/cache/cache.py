import json
from alvinchow.lib.logging import get_logger

logger = get_logger(__name__)


class RedisCache:
    """
    Simple cache using JSON serialization
    """
    def __init__(self, connection):
        self.connection = connection

    def set(self, key, value, expiration=60):
        encoded = json.dumps(value)
        self.connection.set(key, encoded, ex=expiration)

    def get(self, key):
        encoded_bytes = self.connection.get(key)
        if encoded_bytes is None:
            return None

        try:
            encoded_str = encoded_bytes.decode()
            value = json.loads(encoded_str)
            return value
        except UnicodeDecodeError:
            logger.exception('Problem with unicode decode')
            return None
        except json.JSONDecodeError:
            logger.exception('Problem with JSON decoding')
            return None
