import json

import redis

from app.models.crypto_models import SimplifiedCryptoAsset

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def set_cache(key: str, data: dict[str, SimplifiedCryptoAsset], ttl: int = 30) -> None:
    """
    Store data in Redis cache with a specified time-to-live (TTL).

    Args:
        key (str): The cache key under which the data will be stored.
        data (dict[str, SimplifiedCryptoAsset]): The data to cache.
        ttl (int, optional): Time-to-live in seconds. Defaults to 30.
    """
    r.setex(key, ttl, json.dumps(data))


def get_cache(key: str) -> dict[str, SimplifiedCryptoAsset] | None:
    """
    Retrieve data from Redis cache by key.

    Args:
        key (str): The cache key to look up.

    Returns:
        dict[str, SimplifiedCryptoAsset] or None: Cached data if present,
        otherwise None.
    """
    value = r.get(key)
    return json.loads(value) if value else None
