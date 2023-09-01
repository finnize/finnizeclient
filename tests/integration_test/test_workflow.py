from finnizeclient.client.upload_signal import delete_backtest_signals
from finnizeclient.workflow import upload_tradingview_signal


def test_workflow():
    actual = upload_tradingview_signal(
        path="example/list_of_trade_example.csv",
        strategy_id=3145225415244741,
        weight=1,
        url="https://dev-client-gateway.finnize.com/api/v1/strategy-signal/",
    )
    return actual


def test_delete_backtest_signals():
    actual = delete_backtest_signals(
        strategy_id=3145225415244741,
        url="https://dev-client-gateway.finnize.com/api/v1/strategy-signal/",
    )
    return actual
