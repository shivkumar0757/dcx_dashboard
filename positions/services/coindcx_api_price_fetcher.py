from asyncio.log import logger

import requests
import time
from typing import List, Dict, Tuple


class CoinDCXAPIPriceFetcher:
    # Cache to store prices and timestamps
    _price_cache: Dict[str, Tuple[float, float]] = {}  # Format: {pair: (price, timestamp)}

    @staticmethod
    def get_prices_single_api(pair: str) -> float:
        """
        Fetches the latest price for a specific pair from the CoinDCX API.
        """
        api_url = "https://public.coindcx.com/market_data/v3/current_prices/futures/rt"
        response = requests.get(api_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from CoinDCX API. Status Code: {response.status_code}")

        current_prices_json = response.json()
        current_prices = current_prices_json.get('prices', {})

        # Check if the pair is available in the response
        if pair not in current_prices:
            print(f"Pair {pair} not found in CoinDCX API response")
            return 0
        return current_prices[pair]['mp']

    @classmethod
    def get_price(cls, pair: str, price_type: str = 'last', max_trades: int = 5, cache_duration: float = 5.0) -> float:
        """
        Fetches the price for a given pair, using cached data if the cache is not expired.

        :param pair: The trading pair (e.g., 'B-1000PEPE_USDT').
        :param price_type: Type of price to fetch - 'last' or 'average'.
        :param max_trades: Maximum number of trades to consider for averaging.
        :param cache_duration: Cache duration in seconds before fetching new data.
        :return: The price based on the specified price_type.
        """
        current_time = time.time()

        # Check if the pair is in the cache and if the cache is still valid
        if pair in cls._price_cache:
            cached_price, cached_time = cls._price_cache[pair]
            if current_time - cached_time < cache_duration:
                print(f"Returning cached price for {pair}: {cached_price}")
                return cached_price

        # Fetch fresh data from the API and update the cache
        new_price = cls.get_prices_single_api(pair)
        cls._price_cache[pair] = (new_price, current_time)

        print(f"Fetched new price for {pair}: {new_price}")
        return new_price

# class CoinDCXAPIPriceFetcher:
#     @staticmethod
#     def get_prices_single_api(pair: str) -> float:
#         api_url = "https://public.coindcx.com/market_data/v3/current_prices/futures/rt"
#         response = requests.get(api_url)
#         if response.status_code != 200:
#             raise Exception(f"Failed to fetch data from CoinDCX API. Status Code: {response.status_code}")
#         curren_prices_json = response.json()
#         current_prices = curren_prices_json['prices']
#         if pair not in current_prices:
#             logger.error(f"Pair {pair} not found in CoinDCX API response")
#             return 0
#         return current_prices[pair]
#
#
#     @staticmethod
#     def get_price(pair: str, price_type: str = 'last', max_trades: int = 5) -> float:
#         """
#         Fetches the price for a given pair from CoinDCX API.
#
#         :param cls:
#         :param pair: The trading pair (e.g., 'B-1000PEPE_USDT').
#         :param price_type: Type of price to fetch - 'last' or 'average'.
#         :param max_trades: Maximum number of trades to consider for averaging.
#         :return: The price based on the specified price_type.
#         """
#
#         return CoinDCXAPIPriceFetcher.get_prices_single_api(pair)
#
#         # Construct the API URL for the given pair
#         api_url = f"https://api.coindcx.com/exchange/v1/derivatives/futures/data/trades?pair={pair}"
#
#         # Fetch trade data from the API
#         response = requests.get(api_url)
#         if response.status_code != 200:
#             raise Exception(f"Failed to fetch data from CoinDCX API. Status Code: {response.status_code}")
#
#         trade_data = response.json()
#
#         # Get the latest trades up to the specified maximum
#         latest_trades = trade_data[-min(len(trade_data), max_trades):]
#
#         if price_type == 'average':
#             # Consider only trades within the last 2 seconds
#             current_timestamp = int(time.time() * 1000)
#             valid_prices = [trade['price'] for trade in latest_trades if current_timestamp - trade['timestamp'] <= 2000]
#
#             # If there are not enough valid trades, return the last trade's price
#             if len(valid_prices) < max_trades:
#                 return trade_data[-1]['price']
#             return sum(valid_prices) / len(valid_prices)
#
#         # Default to returning the last trade's price
#         return trade_data[-1]['price']


# # Example usage
# try:
#     price = CoinDCXAPIPriceFetcher.get_price(pair='B-1000PEPE_USDT', price_type='last')
#     print(f"Price: {price}")
# except Exception as e:
#     print(f"Error: {e}")
