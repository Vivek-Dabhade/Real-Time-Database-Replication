import time

import requests
from schema import sql_insert_data

# Binance API endpoint for all tickers (full info for BTCUSDT included)
url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"

# while True:
for i in range(15):
    try:
        response = requests.get(url)
        data = response.json()
        # print(data)

        price = data["lastPrice"]
        quantity = data["lastQty"]

        print(f"Price: {data['lastPrice']}, Quantity: {data['lastQty']}")

        sql_insert_data(price, quantity)
        time.sleep(2)

    except KeyboardInterrupt:
        print("\nStopped by user")
        break
    except Exception as e:
        print("\nError:", e)
        time.sleep(2)
