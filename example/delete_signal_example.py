from finnizeclient.client.upload_signal import delete_backtest_signals

"""
The user should be authorized as a guru to be able to upload or delete the backtest signal.
"""
delete_backtest_signals(
    strategy_id=3907697156338858,
    url="https://dev-client-gateway.finnize.com/api/v1/strategy-signal/",
)
