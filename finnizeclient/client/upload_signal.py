import ast
import json

import requests

from finnizeclient import config as cfg

"""
The user should be authorized as a guru to be able to upload or delete the backtest signal.
"""
if ast.literal_eval(cfg.FINNIZE_ENVIRONMENT):
    headers = {
        "X-Permission": json.dumps(
            {
                "role_id": cfg.ROLE_ID,
                "name": cfg.NAME,
                "can_login_admin_site": cfg.CAN_LOGIN_ADMIN_SITE,
                "can_create_strategy": cfg.CAN_CREATE_STRATEGY,
                "user_id": cfg.USER_ID,
                "broker_id": cfg.BROKER_ID,
            }
        )
    }
else:
    headers = {
        "Authorization": f"Bearer {cfg.FINNIZE_API_KEY}.{cfg.FINNIZE_API_SECRET}"
    }


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
    res = requests.post(url=url, json=strategy_signal, timeout=60, headers=headers)
    if not res.ok:
        msg = f"{res.json()}"
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
    res = requests.delete(url=url, json=json_strategy_id, timeout=60, headers=headers)
    if not res.ok:
        msg = f"{res.json()}"
        raise requests.HTTPError(msg)


"""
    LOCAL METHOD ENVIRONMENT
"""
