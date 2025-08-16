import os

import requests
from dotenv import load_dotenv

from app.models.crypto_models import CryptoApiResponse, SimplifiedCryptoAsset

load_dotenv()

API_KEY: str | None = os.getenv("COIN_MARKET_CAP_API_KEY")
API_ENDPOINT = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"


def _fetch_top_cryptos(limit: int) -> CryptoApiResponse | None:
    """
    Fetch the top cryptocurrencies by market capitalization
    from CoinMarketCap API.

    Args:
        limit (int): The number of cryptocurrencies to retrieve.

    Returns:
        CryptoApiResponse or None: TypedDict with API response data
        if successful, or None if an error occurs.

    Raises:
        ValueError: If the CoinMarketCap API key is not set in the
        environment variable COIN_MARKET_CAP_API_KEY.

    Notes:
        - Requires a valid CoinMarketCap API key set in the
        environment variable 'COIN_MARKET_CAP_API_KEY'.
        - Handles network and request exceptions gracefully,
        printing an error message and returning None.
    """
    if not API_KEY:
        raise ValueError(
            "API key for CoinMarketCap is not set. "
            "Please set the COIN_MARKET_CAP_API_KEY environment variable."
        )

    try:
        response: requests.Response = requests.get(
            API_ENDPOINT,
            params={
                "sort": "market_cap",
                "sort_dir": "desc",
                "limit": limit,
                "convert": "USD",
            },
            headers={
                "Accept": "application/json",
                "Accept-Encoding": "deflate, gzip",
                "X-CMC_PRO_API_KEY": API_KEY,
            },
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")


def _parse_crypto_data(
    json_response: CryptoApiResponse,
) -> dict[str, SimplifiedCryptoAsset]:
    """
    Parse the cryptocurrency data from the API response.

    Args:
        json_response (CryptoApiResponse): The JSON response
        from the CoinMarketCap API.

    Returns:
        list[SimplifiedCryptoAsset]: List of simplified cryptocurrency assets
        with name, symbol, and price in USD.
    """
    return {
        str(idx + 1): {
            "name": coin["name"],
            "symbol": coin["symbol"],
            "usd_price": round(coin["quote"]["USD"]["price"], 2),
        }
        for idx, coin in enumerate(json_response.get("data", []))
    }


def get_parsed_crypto_data(limit: int = 10) -> dict[str, SimplifiedCryptoAsset] | None:
    """
    Retrieve and parse the top cryptocurrencies from the CoinMarketCap API.

    Args:
        limit (int, optional): The number of cryptocurrencies to retrieve.
        Defaults to 10.

    Returns:
        dict[str, SimplifiedCryptoAsset] or None: Dictionary where keys
        are rankings (as strings) and values are simplified
        crypto asset data (name, symbol, usd_price). Returns None if the API call fails.
    """
    response = _fetch_top_cryptos(limit=limit)
    return _parse_crypto_data(response) if response else None
