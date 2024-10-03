import requests
import time
from typing import List


class CoinDCXAPIPriceFetcher:
    @staticmethod
    def get_price(pair: str, price_type: str = 'last', max_trades: int = 5) -> float:
        """
        Fetches the price for a given pair from CoinDCX API.

        :param pair: The trading pair (e.g., 'B-1000PEPE_USDT').
        :param price_type: Type of price to fetch - 'last' or 'average'.
        :param max_trades: Maximum number of trades to consider for averaging.
        :return: The price based on the specified price_type.
        """
        # Construct the API URL for the given pair
        api_url = f"https://api.coindcx.com/exchange/v1/derivatives/futures/data/trades?pair={pair}"

        # Fetch trade data from the API
        response = requests.get(api_url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from CoinDCX API. Status Code: {response.status_code}")

        trade_data = response.json()

        # Get the latest trades up to the specified maximum
        latest_trades = trade_data[-min(len(trade_data), max_trades):]

        if price_type == 'average':
            # Consider only trades within the last 2 seconds
            current_timestamp = int(time.time() * 1000)
            valid_prices = [trade['price'] for trade in latest_trades if current_timestamp - trade['timestamp'] <= 2000]

            # If there are not enough valid trades, return the last trade's price
            if len(valid_prices) < max_trades:
                return trade_data[-1]['price']
            return sum(valid_prices) / len(valid_prices)

        # Default to returning the last trade's price
        return trade_data[-1]['price']


# # Example usage
# try:
#     price = CoinDCXAPIPriceFetcher.get_price(pair='B-1000PEPE_USDT', price_type='last')
#     print(f"Price: {price}")
# except Exception as e:
#     print(f"Error: {e}")
