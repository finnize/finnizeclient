from src.workflow import upload_tradingview_signal

# Before uploading any signals to the Finnize website, you need to know the `strategy_id`.
# The weight should be between 0 and 1. A value of 1 signifies a full Long or Short entry (100%).
upload_tradingview_signal(
    path="list_of_trade_example.csv",
    strategy_id=1,
    weight=1,
    url="https://dev-client-gateway.finnize.com/api/v1/strategy-signal/",
)
