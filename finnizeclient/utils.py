from pathlib import Path

import numpy as np
import pandas as pd
import pytz


def read_list_of_trades(path: str):
    df = pd.read_csv(Path(path))
    return df


def _format_datetime(signal_list: list[dict]) -> list[dict]:
    """Format datetime strings in a list of signal dictionaries to UTC with the format
    '%Y-%m-%dT%H:%M:Z'.

    Parameters
    ----------
    signal_list : list[dict]
        A list of dictionaries containing signal information.

    Returns
    -------
    list[dict]
        A list of dictionaries with formatted datetime strings in UTC and signal data.

    Notes
    -----
    This function takes a list of dictionaries, each representing a signal with a 'signal_at' datetime
    string and a 'signal' dictionary. It converts the 'signal_at' datetime strings from the provided
    timezone (Asia/Bangkok) to UTC and formats them using the '%Y-%m-%dT%H:%M:Z' format.

    Example
    -------
    >>> signal_list = [
        {'signal_at': '2023-08-07 13:00', 'signal': {'S50': 0.0}},
        {'signal_at': '2023-08-04 17:45', 'signal': {'S50': -0.5}}
    ]
    >>> formatted_signals = _formate_datetime(signal_list)
    >>> print(formatted_signals)
        [
            {'signal_at': '2023-08-07T06:00:Z', 'signal': {'S50': 0.0}},
            {'signal_at': '2023-08-04T10:45:Z', 'signal': {'S50': -0.5}}
        ]
    """
    timezone_utc_plus_7 = pytz.timezone("Asia/Bangkok")
    formatted_signals = [
        {
            "signal_at": pd.to_datetime(item["signal_at"])
            .tz_localize(timezone_utc_plus_7)
            .astimezone(pytz.UTC)
            .strftime("%Y-%m-%dT%H:%M:"), # วิธีใส่ timezone ผ่าน stff
            "signal": item["signal"],
        }
        for item in signal_list
    ]
    return formatted_signals


def transform_list_of_trades(df: pd.DataFrame, strategy_id: int, weight: float) -> dict:
    """Transforms a DataFrame of trades into a dictionary of signals for a given
    strategy.

    This function takes a DataFrame containing trade information and processes the data,
    assigning trade actions based on the provided weight value:
    - Weight 0 indicates a "sell" action.
    - Positive weights represent "long" positions.
    - Negative weights represent "short" positions.

    Parameters
    ----------
    df : str
        DataFrame containing trade information with columns: 'Type', 'Date/Time'.
    strategy_id : int
        Identifier for the strategy associated with the signals.
    weight : float
        Weight to be assigned to specific trade types.

    Returns
    -------
    dict
        A dictionary containing the strategy ID and a list of dictionaries representing signals.

    Examples
    -------
    >>> signals = transform_list_of_trades("trades.csv", 999, 0.5)
    >>> print(signals)
    {'strategy_id': 999,
     'signals': [{'signal_at': '2023-08-07 13:00', 'signal': {'S50': 0.0}},
                 {'signal_at': '2023-08-04 17:45', 'signal': {'S50': -0.5}},
                 {'signal_at': '2023-08-03 10:45', 'signal': {'S50': 0.0}},
                 {'signal_at': '2023-08-03 10:45', 'signal': {'S50': -0.5}},
                 {'signal_at': '2023-07-14 16:45', 'signal': {'S50': 0.0}}]
    }
    """
    # transform to weight
    df.loc[df["Type"].isin(["Exit Short", "Exit Long"]), "weight"] = 0  # sell
    df.loc[df["Type"].isin(["Entry Long"]), "weight"] = weight
    df.loc[df["Type"].isin(["Entry Short"]), "weight"] = -weight

    # generate list signals
    signals_list = []
    for _index, row in df.iterrows():
        signal = {"signal_at": np.nan, "signal": {}}  # format for each signals
        signal["signal_at"] = row["Date/Time"]
        signal["signal"]["S50"] = row["weight"]
        signals_list.append(signal)

    # check the latest signal is holding or not
    if isinstance(signals_list[0]["signal_at"], float):
        signals_list.pop(0)

    # convert and format datetime as UTC+0
    formatted_signals = _format_datetime(signal_list=signals_list)

    # transform as a dictionary signals
    strategy_signal = {"strategy_id": strategy_id, "signals": formatted_signals}
    return strategy_signal
