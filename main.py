from time import sleep
from datetime import datetime, timezone
from tracemalloc import start

from pymongo import ASCENDING, DESCENDING, errors

from kucoin_api import get_tickers, get_klines
from mongo import client
from settings import PAIRS, CANDLE_TYPES, START_TIME
from utils import progress_bar, date_to_str


candle_type_seconds = {
        "1min": 60,
        "3min": 180,
        "5min": 300,
        "15min": 900,
        "30min": 1800,
        "1hour": 3600,
        "2hour": 7200,
        "4hour": 14400,
        "6hour": 21600,
        "8hour": 28800,
        "12hour": 43200,
        "1day": 86400,
        "1week": 604800
    }


def import_candles_data(pair, candle, candle_col, start_time, end_time, time_delta):
    # Query all the candles from start to end
    print(f"Querying Klines {candle} for {pair} from {date_to_str(start_time)} to {date_to_str(end_time)}:", end="\n")

    actual_time = start_time
    progress_bar(start_time, end_time, actual_time)

    while actual_time < end_time:
        try:
            if end_time <= actual_time + time_delta:
                # Avoid going over the end_time
                klines = get_klines(pair, candle, actual_time, end_time)
            else:
                klines = get_klines(pair, candle, actual_time, actual_time + time_delta)

        except Exception as e:
            print(f"\rError occured: {e}, trying again...")
            sleep(15)
            continue
        
        if klines:
            candle_col.insert_many(klines)
        
        actual_time += time_delta
        progress_bar(start_time, end_time, actual_time)
        sleep(5)


def main():
    # Check tickers exists and remove inexistant ones
    tickers = get_tickers()
    pairs = list(set(PAIRS).intersection(tickers))

    
    for pair in pairs:
        
        # Get or create the DB for a pair
        db = client[pair]

        for candle in CANDLE_TYPES:

            candle_seconds = candle_type_seconds[candle]
            time_delta = candle_seconds * 1500 # Kucoin's candle limit per query
            if not candle_seconds:
                continue

            # Define start and end time based on candle timespan
            start_time = START_TIME // candle_seconds * candle_seconds
            # At best we get the last finished candle to avoir having to update them later
            end_time =  int(datetime.now(timezone.utc).timestamp()) // candle_seconds * candle_seconds - candle_seconds

            
            # Get or create a collection for the candle size
            candle_col = db[candle]
            candle_col.create_index([("time", DESCENDING)], unique=True)

            # Verify if the collection is a new one
            if not candle_col.count_documents({}):
                print(f"\nInitial update for {pair} in format {candle}.")
                import_candles_data(pair, candle, candle_col, start_time, end_time, time_delta)

            else:
                # Get the latter and older candles to define the missing data
                latter = candle_col.find_one(sort=[("time", DESCENDING)])
                
                # New candles are available
                if latter["time"] + candle_seconds < end_time:
                    print(f"\nNew data to be updated for {pair} in format {candle}.")
                    import_candles_data(pair, candle, candle_col, latter["time"] + candle_seconds, end_time, time_delta)

                older = candle_col.find_one(sort=[("time", ASCENDING)])

                # Settings have been adjusted to query older data
                if start_time < older["time"]:
                    print(f"\nAdding older data for {pair} in format {candle}.")
                    import_candles_data(pair, candle, candle_col, start_time, older["time"] - candle_seconds, time_delta)


if __name__ == "__main__":
    main()