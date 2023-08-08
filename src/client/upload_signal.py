import requests


def upload_backtest_signals(strategy_signal: dict):
    """Upload the signal to finnize website.

    Parameters
    ----------
    strategy_signal : dict
        A dictionary containing the strategy ID and a list of dictionaries representing signals.

    Raises
    ------
    None
        Returns None if the upload is successful.
    """
    res = requests.post(
        url="https://dev-client-gateway.finnize.com/api/v1/strategy-signal/",
        json=strategy_signal,
        # note: add the API KEY and SECRET later.
    )
    if not res.ok:
        msg = f"{res.json()}"
        raise Exception(msg)
