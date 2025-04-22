import numpy as np
import pandas as pd
import pytest
from pandas._testing import assert_dict_equal

from finnizeclient.utils import (
    transform_list_of_trades,
)

tz_info = pd.Timestamp("2023-08-04T10:00+0700").tzinfo


class TestTransformListOfTrade:
    @pytest.mark.parametrize(
        ("df", "expect_result"),
        [
            # case 1: The most recent indication is already sell.
            (
                pd.DataFrame(
                    data=[
                        ["Entry short", pd.to_datetime("2023-08-04 10:00"), "1,000.0"],
                        ["Exit short", pd.to_datetime("2023-08-05 10:00"), "2,000.0"],
                        ["Entry long", pd.to_datetime("2023-08-06 10:00"), "3,000.0"],
                        ["Exit long", pd.to_datetime("2023-08-07 10:00"), "4,000.0"],
                    ],
                    columns=["Type", "Date/Time", "Price THB"],
                ),
                {
                    "strategy_id": 10,
                    "signals": [
                        {
                            "signal_at": "2023-08-04T10:00+0700",
                            "signal": {"S50": -0.5},
                            "price": {"S50": 1000.0},
                        },
                        {
                            "signal_at": "2023-08-05T10:00+0700",
                            "signal": {"S50": 0.0},
                            "price": {"S50": 2000.0},
                        },
                        {
                            "signal_at": "2023-08-06T10:00+0700",
                            "signal": {"S50": 0.5},
                            "price": {"S50": 3000.0},
                        },
                        {
                            "signal_at": "2023-08-07T10:00+0700",
                            "signal": {"S50": 0.0},
                            "price": {"S50": 4000.0},
                        },
                    ],
                },
            ),
            # case 2: The newest indication is holding.
            (
                pd.DataFrame(
                    data=[
                        ["Entry long", pd.to_datetime("2023-08-03 10:45"), "1,000.0"],
                        ["Exit long", pd.to_datetime("2023-08-03 12:45"), "2,000.0"],
                        ["Entry short", pd.to_datetime("2023-08-03 17:45"), "3,000.0"],
                        ["Exit short", np.nan, np.nan],
                    ],
                    columns=["Type", "Date/Time", "Price THB"],
                ),
                {
                    "strategy_id": 10,
                    "signals": [
                        {
                            "signal_at": "2023-08-03T10:45+0700",
                            "signal": {"S50": 0.5},
                            "price": {"S50": 1000.0},
                        },
                        {
                            "signal_at": "2023-08-03T12:45+0700",
                            "signal": {"S50": 0.0},
                            "price": {"S50": 2000.0},
                        },
                        {
                            "signal_at": "2023-08-03T17:45+0700",
                            "signal": {"S50": -0.5},
                            "price": {"S50": 3000.0},
                        },
                    ],
                },
            ),
            # case 3: The daily signal format
            (
                pd.DataFrame(
                    data=[
                        ["Entry long", pd.to_datetime("2023-08-02"), "1,000.0"],
                        ["Exit long", pd.to_datetime("2023-08-03"), "2,000.0"],
                        ["Entry short", pd.to_datetime("2023-08-04"), "3,000.0"],
                    ],
                    columns=["Type", "Date/Time", "Price THB"],
                ),
                {
                    "strategy_id": 10,
                    "signals": [
                        {
                            "signal_at": "2023-08-02T00:00+0700",
                            "signal": {"S50": 0.5},
                            "price": {"S50": 1000.0},
                        },
                        {
                            "signal_at": "2023-08-03T00:00+0700",
                            "signal": {"S50": 0.0},
                            "price": {"S50": 2000.0},
                        },
                        {
                            "signal_at": "2023-08-04T00:00+0700",
                            "signal": {"S50": -0.5},
                            "price": {"S50": 3000.0},
                        },
                    ],
                },
            ),
        ],
    )  # type: ignore
    def test_success_normal_case(self, df: pd.DataFrame, expect_result: dict):
        result = transform_list_of_trades(df=df, strategy_id=10, weight=0.5)
        # Check
        return assert_dict_equal(result, expect_result)
