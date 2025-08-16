from typing import Dict, List, TypedDict


class USDQuote(TypedDict):
    price: float


class Quote(TypedDict):
    USD: USDQuote


class CryptoDataItem(TypedDict):
    name: str
    symbol: str
    quote: Quote


class CryptoApiResponse(TypedDict):
    status: Dict[str, str]
    data: List[CryptoDataItem]


class SimplifiedCryptoAsset(TypedDict):
    name: str
    symbol: str
    usd_price: float
