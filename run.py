from src.workflow import upload_tradingview_signal

# enter the path, strategy_id, weight and url before uploading signals
upload_tradingview_signal(
    path="example/list_of_trade_example.csv",
    strategy_id=1,
    weight=1,
    url="https://dev-client-gateway.finnize.com/api/v1/strategy-signal/",
)
