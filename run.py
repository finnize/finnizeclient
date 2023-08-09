import logging.config

import yaml

from src.workflow import upload_tradingview_signal

# Load the config file
with open("logging_config.yaml") as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)

# enter the path, strategy_id, weight and url before uploading signals
upload_tradingview_signal(
    path="example/list_of_trade_example.csv",
    strategy_id=3907697156338858,
    weight=1,
    url="https://dev-client-gateway.finnize.com/api/v1/strategy-signal/",
)
