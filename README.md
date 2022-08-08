# kucoin-klines
Query Kucoin's klines data and store it in MongoDB.

As Kucoin kline endpoint is limited to 1500 rows per call, a better way to use OHLCV data is to store it.
Kucoin credentials aren't required as those are public endpoints.

## Install

```
git clone git@github.com:gudlc/kucoin-klines.git
```

### Install reqquirements
```
pip install -r requirements.txt
```

### Settings

The script will collect only the datas you request, rename settings.py.sample to settings.py
Then add the pairs and candle types you're interested in.

##### Supported ```Candle Type``` values:
```1min```
```3min```
```5min```
```15min```
```30min```
```1hour```
```2hour```
```4hour```
```6hour```
```8hour```
```12hour```
```1day```
```1week```

You can change the start time if you need older data, the older you can get is 1566789720.
```
START_TIME = 1566789720
```

## Run the script
```
python main()
```

The script will only query completed klines and you can always launch it again to fetch new data.


### Useful Links:
- https://www.unixtimestamp.com
- https://docs.kucoin.com/#get-klines


Inspired from https://github.com/krnewberry/KuLine, thanks ;)
