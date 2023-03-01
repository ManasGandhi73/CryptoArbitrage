import requests
import time

# Constants
COIN = "USDC"  # Change to the stablecoin you want to trade
BUY_THRESHOLD = 1.00  # Price threshold to trigger a buy order
SELL_THRESHOLD = 1.00  # Price threshold to trigger a sell order
AMOUNT = 30  # Amount of USD to invest per buy order

# Coinbase API endpoint URLs
COINBASE_API_URL = "https://api.coinbase.com/v2"
PRICE_ENDPOINT = f"{COINBASE_API_URL}/prices/{COIN}-USD/spot"
ACCOUNTS_ENDPOINT = f"{COINBASE_API_URL}/accounts"
ORDERS_ENDPOINT = f"{COINBASE_API_URL}/orders"

# Coinbase API authentication
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
API_PASSPHRASE = "your_api_passphrase"

# Coinbase API headers
headers = {
    "Content-Type": "application/json",
    "CB-ACCESS-KEY": API_KEY,
    "CB-ACCESS-SIGN": "",
    "CB-ACCESS-TIMESTAMP": "",
    "CB-ACCESS-PASSPHRASE": API_PASSPHRASE,
}

# Get current price of the stablecoin
def get_coin_price():
    response = requests.get(PRICE_ENDPOINT)
    price = float(response.json()["data"]["amount"])
    return price

# Get ID of the USD account
def get_usd_account_id():
    response = requests.get(ACCOUNTS_ENDPOINT, headers=headers)
    accounts = response.json()["data"]
    for account in accounts:
        if account["currency"] == "USD" and account["type"] == "fiat":
            account_id = account["id"]
            return account_id
    return None

# Get ID of the stablecoin account
def get_coin_account_id():
    response = requests.get(ACCOUNTS_ENDPOINT, headers=headers)
    accounts = response.json()["data"]
    for account in accounts:
        if account["currency"] == COIN:
            account_id = account["id"]
            return account_id
    return None

# Buy the stablecoin with USD
def buy_coin():
    usd_account_id = get_usd_account_id()
    coin_account_id = get_coin_account_id()
    buy_price = get_coin_price()
    buy_amount = round(AMOUNT / buy_price, 8)
    payload = {
        "type": "market",
        "side": "buy",
        "product_id": f"{COIN}-USD",
        "funds": str(AMOUNT),
        "size": str(buy_amount),
        "price": str(buy_price),
        "time_in_force": "GTC",
    }
    response = requests.post(ORDERS_ENDPOINT, headers=headers, json=payload)
    print(response.json())

# Sell all assets of the stablecoin
def sell_all_coin():
    coin_account_id = get_coin_account_id()
    sell_price = get_coin_price()
    payload = {
        "type": "market",
        "side": "sell",
        "product_id": f"{COIN}-USD",
        "funds": "all",
        "size": "all",
        "price": str(sell_price),
        "time_in_force": "GTC",
    }
    response = requests.post(ORDERS_ENDPOINT, headers=headers, json=payload)
    print(response.json())

# Main loop
while True:
    price = get_coin_price()
    if price < BUY_THRESHOLD:
        buy_coin()
        while price < SELL_THRESHOLD:
            price = get_coin_price()
