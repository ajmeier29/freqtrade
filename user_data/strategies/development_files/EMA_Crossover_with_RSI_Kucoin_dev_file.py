from pathlib import Path
from freqtrade.configuration import Configuration
from freqtrade.data.history import load_pair_history
from freqtrade.resolvers import StrategyResolver
from freqtrade.data.dataprovider import DataProvider

# Customize these according to your needs.

# Initialize empty configuration object
config = Configuration.from_files(["./configs/kucoin/kucoin-btc-eth-config.json"])
# Optionally, use existing configuration file
# config = Configuration.from_files(["config.json"])

# Define some constants
config["timeframe"] = "5m"
# Name of the strategy class
config["strategy"] = "EMA_Crossover_with_RSI"
# Location of the data
data_location = Path(config['user_data_dir'], 'data', 'kucoin')
# Pair to analyze - Only use one pair here
pair = "BTC_USDT"

candles = load_pair_history(datadir=data_location,
                            timeframe=config["timeframe"],
                            pair=pair,
                            #data_format = "hdf5",
                            )

# Confirm success
print("Loaded " + str(len(candles)) + f" rows of data for {pair} from {data_location}")
candles.head()

strategy = StrategyResolver.load_strategy(config)
strategy.dp = DataProvider(config, None, None)

# Generate buy/sell signals using strategy
df = strategy.analyze_ticker(candles, {'pair': pair})
df.tail()

print(f"""

        Generated {df['buy'].sum()} buy signals
        Generated {df['sell'].sum()} sell signals
        """)
data = df.set_index('date', drop=False)
data.tail()