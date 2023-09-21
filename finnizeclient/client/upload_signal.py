import requests
from requests.auth import HTTPBasicAuth

from finnizeclient import config as cfg

"""
The user should be authorized as a guru to be able to upload or delete the backtest signal.
"""


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
    requests.HTTPError
        Returns None if the upload is successful.
    """
    res = requests.post(
        url=url,
        json=strategy_signal,
        timeout=60,
        auth=HTTPBasicAuth(
            username=cfg.FINNIZE_API_KEY, password=cfg.FINNIZE_API_SECRET
        ),
    )
    if not res.ok:
        msg = f"{res.text}"
        raise requests.HTTPError(msg)


def delete_backtest_signals(strategy_id: int, url: str):
    """Delete the all signal of the strategy_id on finnize website.

    Parameters
    ----------
    strategy_id : int
        number of strategy_id.
    url : str
        The URL endpoint where the signals will be uploaded.
    Raises
    ------
    requests.HTTPError
        Returns None if the upload is successful.
    """
    json_strategy_id = {"strategy_id": strategy_id}
    res = requests.delete(
        url=url,
        json=json_strategy_id,
        timeout=60,
        auth=HTTPBasicAuth(
            username=cfg.FINNIZE_API_KEY, password=cfg.FINNIZE_API_SECRET
        ),
    )
    if not res.ok:
        msg = f"{res.text}"
        raise requests.HTTPError(msg)
