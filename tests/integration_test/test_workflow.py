from src.workflow import upload_tradingview_signal


def test_workflow():
    acutal = upload_tradingview_signal(
        path="example/list_of_trade_example.csv",
        strategy_id=3907697156338858,
        weight=1,
        url="https://dev-client-gateway.finnize.com/api/v1/strategy-signal/",
    )
    return acutal
