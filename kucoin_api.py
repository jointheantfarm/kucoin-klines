import requests


url = "https://api.kucoin.com"


def get_tickers():
    response = requests.get(f"{url}/api/v1/symbols")
    data = response.json()
    if data["code"] == '200000':
        return [pair["symbol"] for pair in data["data"]]
    else:
        return []


def get_klines(pair, candle, start_time, end_time):
    # Must use the end_time parameter because of potential empty candles
    params = {
        "symbol": pair,
        "startAt": start_time,
        "endAt": end_time,
        "type": candle
    }
    response = requests.get(f"{url}/api/v1/market/candles", params=params)
    data = response.json()

    if data["code"] == '200000':
        return [{
            "time": int(candle[0]),
            "open": candle[1],
            "close": candle[2],
            "high": candle[3],
            "low": candle[4],
            "volume": candle[5],
            "turnover": candle[6]
        } for candle in data["data"]]

    
    elif data["code"] == '429000':
        raise Exception("Too many requests")

    else:
        print(data)
        raise Exception("Error while getting klines data")