import time

from app.models.crypto_models import SimplifiedCryptoAsset
from app.services.api_call import get_parsed_crypto_data
from app.services.cache import get_cache, set_cache


def get_cached_crypto_data() -> dict[str, SimplifiedCryptoAsset]:
    """
    Retrieve cryptocurrency data from cache if available;
    otherwise, fetch from API and cache the result.

    Returns:
        dict[str, SimplifiedCryptoAsset]: Dictionary of simplified
        crypto assets keyed by ranking as strings.

    Raises:
        Exception: If data cannot be fetched from the API.
    """
    cached_data = get_cache("top_cryptos")
    if cached_data:
        print("CACHE HIT")
        return cached_data
    else:
        print("CACHE MISS")
        data = get_parsed_crypto_data(limit=15)
        if data:
            set_cache("top_cryptos", data, ttl=10)
            return data
        else:
            raise Exception("Failed to fetch data from API")


if __name__ == "__main__":
    # Simulate multiple calls at different times to demonstrate caching
    for _ in range(4):
        data = get_cached_crypto_data()
        print(data)
        time.sleep(4)
