from datetime import datetime
from pathlib import Path

import pandas as pd
from dateutil.tz import tzlocal

formats = [
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
]


def read_list_of_trades(path: str):
    """The default sorting order for the trade list on TradingView is from newest to
    oldest.

    Therefore, we need to rearrange it to display the trades from oldest to newest.
    """
    return pd.read_excel(Path(path), sheet_name="List of trades")


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
    -------
    >>> signals = transform_list_of_trades("trades.csv", 999, 0.5)
    >>> print(signals)
    {'strategy_id': 999,
     'signals': [{'signal_at': '2023-08-07T13:00+0700', 'signal': {'S50': 0.0}},
                 {'signal_at': '2023-08-04T14:00+0700', 'signal': {'S50': -0.5}},
                 {'signal_at': '2023-08-03T15:00+0700', 'signal': {'S50': 0.0}},
                 {'signal_at': '2023-08-03T16:00+0700', 'signal': {'S50': -0.5}},
                 {'signal_at': '2023-07-14T17:00+0700', 'signal': {'S50': 0.0}}]
    }
    """
    # Convert column names to lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Transform signal_at
    if utc.startswith("UTC+"):
        tz = "Etc/GMT-" + utc[4:]
    elif utc.startswith("UTC-"):
        tz = "Etc/GMT+" + utc[4:]
    else:
        raise ValueError(
            "Invalid UTC format. Use 'UTC+X' or 'UTC-X' where X is the offset."
        )
    signal_at_sr = df["date/time"].dt.tz_localize(tz).dt.to_pydatetime()

    # Transform weight
    is_long = df["type"] == "Entry Long"
    is_short = df["type"] == "Entry Short"

    signal_sr = (is_long * weight) - (is_short * weight)

    # Fix price column name
    price_sr = df.filter(like="price_").iloc[:, 0]
    price_sr = price_sr.str.replace(",", "").astype(float)

    def to_dict(signal_at, signal, price):
        return {
            "signal_at": signal_at,
            "signal": {"S50": signal},
            "price": {"S50": price},
        }

    signals = [
        to_dict(signal_at, signal, price)
        for signal_at, signal, price in zip(signal_at_sr, signal_sr, price_sr)
    ]

    return {"strategy_id": strategy_id, "signals": signals}


def get_current_datetime() -> datetime:
    return datetime.now(tz=tzlocal()).strftime("%Y-%m-%dT%H:%M%z")
