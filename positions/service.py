import hmac
import hashlib
import json
import time
import requests
import logging

logger = logging.getLogger(__name__)

COINDCX_API_URL = 'https://api.coindcx.com/exchange/v1/derivatives/futures/positions'

def fetch_positions(api_key, api_secret, margin_currency_short_name=None):
    try:
        timestamp = int(time.time() * 1000)
        body = {
            "timestamp": timestamp,
            "page": "1",
            "size": "50",
            "margin_currency_short_name": margin_currency_short_name or ["USDT", "INR"]
        }
        json_body = json.dumps(body, separators=(',', ':'))
        secret_bytes = bytes(api_secret, encoding='utf-8')
        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': api_key,
            'X-AUTH-SIGNATURE': signature
        }

        response = requests.post(COINDCX_API_URL, data=json_body, headers=headers)
        logger.info(f"CoinDCX API response: {response.text}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching positions from CoinDCX API: {e}")
        raise
