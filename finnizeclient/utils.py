from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from dateutil import tz

formats = [
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
]


def read_list_of_trades(path: str):
    df = pd.read_csv(Path(path))
    return df


def _parse_datetime(input_str: str) -> datetime:
    """Parse a datetime string using a list of possible formats.

    Parameters
    ----------
    input_str : str
        The input datetime string to be parsed.

    Returns
    -------
    datetime
        The parsed datetime object.

    Raises
    ------
    ValueError
        If the input datetime string cannot be parsed using any of the provided formats.
    """
    for format_str in formats:
        try:
            dt_object = datetime.strptime(input_str, format_str)
            return dt_object
        except ValueError:
            pass

    msg = "Invalid datetime format"
    raise ValueError(msg)


def _format_datetime(signal_list: list[dict], utc="UTC+7") -> list[dict]:
    """Format datetime strings in a list of signal dictionaries to UTC with the format
    '%Y-%m-%dT%H:%M:Z'.

    Parameters
    ----------
    signal_list : list[dict]
        A list of dictionaries containing signal information.

    utc : str, optional
        The UTC offset in the format 'UTC±X', where X is the offset in hours. Default is 'UTC+7'.

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
    >>> formatted_signals = _format_datetime(signal_list)
    >>> print(formatted_signals)
        [
            {'signal_at': '2023-08-07T13:00+0700', 'signal': {'S50': 0.0}},
            {'signal_at': '2023-08-04T17:45+0700', 'signal': {'S50': -0.5}}
        ]
    """
    offset = 7 - int(utc.split("UTC")[1][:2])
    formatted_signals = [
        {
            "signal_at": (_parse_datetime(item["signal_at"]) + timedelta(hours=offset))
            .replace(tzinfo=tz.gettz("Etc/GMT-7"))
            .strftime("%Y-%m-%dT%H:%M%z"),
            "signal": item["signal"],
        }
        for item in signal_list
    ]
    return formatted_signals


def _handle_duplicate_signal_at(signal_list: list[dict]):
    """Filter out duplicate signal_at entries while keeping signal <= 0.

    Parameters
    ----------
    signal_list : list[dict]
        A list of dictionaries containing signal data.

    Returns
    -------
    list[dict]
        A filtered list of dictionaries with duplicate signal_at entries removed
        and signal values <= 0.

    Notes
    --------
    This function handles cases where an entry has a signal, and during the same interval period,
    the price hits the stop loss. In backtesting, such signals are rejected
    because the backtesting algorithm processes only OHLC prices.
    However, in actual execution, this issue does not pose a problem.

    Examples
    --------
    >>> data = [
    ...     {"signal_at": "2023-08-04T00:00+0700", "signal": {'S50': 0.0}},
    ...     {"signal_at": "2023-08-05T00:00+0700", "signal": {'S50': 0.5}},
    ...     {"signal_at": "2023-08-06T00:00+0700", "signal": {'S50': 0.0}},
    ...     {"signal_at": "2023-08-06T00:00+0700", "signal": {'S50': 0.5}},
    ... ]
    >>> result = _handle_duplicate_signal_at(data)
    >>> print(result)
    [{'signal_at': '2023-08-04T00:00+0700', 'signal': {'S50': 0.0}},
     {'signal_at': '2023-08-05T00:00+0700', 'signal': {'S50': 0.5}},
     {'signal_at': '2023-08-06T00:00+0700', 'signal': {'S50': 0.0}}]
    """
    seen_dates = set()
    filtered_data = []

    for item in signal_list:
        signal_at = item["signal_at"]
        signal_value = next(iter(item["signal"].values()))  # Extract the signal value
        if signal_at in seen_dates and signal_value > 0:
            continue  # Skip duplicates with signal > 0
        elif signal_at in seen_dates and signal_value == 0:
            # Remove any existing entry with the same signal_at
            filtered_data = [
                entry for entry in filtered_data if entry["signal_at"] != signal_at
            ]
            seen_dates.remove(signal_at)

        seen_dates.add(signal_at)
        filtered_data.append(item)
    return filtered_data


def transform_list_of_trades(
    df: pd.DataFrame, strategy_id: int, weight: float, utc="UTC+7"
) -> dict:
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
    --------
    >>> data = [
    ...     {"signal_at": "2023-08-04 13:00", "signal": {'S50': 0.0}},
    ...     {"signal_at": "2023-08-04 14:00", "signal": {'S50': 1.0}},
    ...     {"signal_at": "2023-08-04 15:00", "signal": {'S50': 1.0}},
    ...     {"signal_at": "2023-08-04 15:00", "signal": {'S50': 0.0}}
    ... ]
    >>> result = _handle_duplicate_signal_at(data)
    >>> print(result)
        [
            {'signal_at': '2023-08-04 13:00', 'signal': {'S50': 0.0}},
            {'signal_at': '2023-08-04 14:00', 'signal': {'S50': 1.0}},
            {'signal_at': '2023-08-04 15:00', 'signal': {'S50': 0.0}}
        ]
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

    # convert and format datetime as UTC+7 ("%Y-%m-%dT%H:%M%z")
    formatted_signals = _format_datetime(signal_list=signals_list, utc=utc)
    # handle duplicate signal_at
    filter_signals = _handle_duplicate_signal_at(signal_list=formatted_signals)
    # transform as a dictionary signals
    strategy_signal = {"strategy_id": strategy_id, "signals": filter_signals}
    return strategy_signal
