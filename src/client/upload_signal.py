import requests


def upload_backtest_signals(strategy_signal: dict, url: str):
    """Upload the signal to finnize website.

    Parameters
    ----------
    strategy_signal : dict
        A dictionary containing the strategy ID and a list of dictionaries representing signals.
    url : str
        The URL endpoint where the signals will be uploaded.
    Raises
    ------
    None
        Returns None if the upload is successful.
    """
    res = requests.post(
        url=url,
        json=strategy_signal,
        # note: add the API KEY and SECRET later.
    )
    if not res.ok:
        msg = f"{res.json()}"
        raise Exception(msg)
