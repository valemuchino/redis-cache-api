import os

import requests
from dotenv import load_dotenv
from models import CryptoApiResponse, SimplifiedCryptoAsset

load_dotenv()

API_KEY: str | None = os.getenv("COIN_MARKET_CAP_API_KEY")
API_ENDPOINT = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"


def fetch_top_cryptos(limit: int = 10) -> CryptoApiResponse | None:
    """
    Fetch the top cryptocurrencies by market capitalization
    from CoinMarketCap API.

    Args:
        limit (int, optional): The number of cryptocurrencies to retrieve.
        Defaults to 10.

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


def parse_crypto_data(json_response: CryptoApiResponse) -> list[SimplifiedCryptoAsset]:
    """
    Parse the cryptocurrency data from the API response.

    Args:
        json_response (CryptoApiResponse): The JSON response
        from the CoinMarketCap API.

    Returns:
        list[SimplifiedCryptoAsset]: List of simplified cryptocurrency assets
        with name, symbol, and price in USD.
    """
    return [
        {
            "name": coin["name"],
            "symbol": coin["symbol"],
            "usd_price": round(coin["quote"]["USD"]["price"], 2),
        }
        for coin in json_response.get("data", [])
    ]


response = fetch_top_cryptos()
if response:
    print(response)
