from finnizeclient.workflow import upload_tradingview_signal

"""
The user should be authorized as a guru to be able to upload or delete the backtest signal.

Before uploading any signals to the Finnize website, you need to know the `strategy_id`.
The weight should be between 0 and 1. A value of 1 signifies a full Long or Short entry (100%).

Enter the path, strategy_id, weight and url before uploading signals
"""
upload_tradingview_signal(
    path="example/list_of_trade_example.csv",
    strategy_id=3907697156338858,
    weight=1,
    utc="UTC+7",
    url="https://dev-client-gateway.finnize.com/api/v1/strategy-signal/",
)
