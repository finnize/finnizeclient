import numpy as np
import pandas as pd
import pytest
from pandas._testing import assert_dict_equal

from finnizeclient.utils import _format_datetime, transform_list_of_trades


class TestTransformListOfTrade:
    @pytest.mark.parametrize(
        ("df", "expect_result"),
        [
            # case 1: The most recent indication is already sell.
            (
                pd.DataFrame(
                    data=[
                        ["Exit Short", "2023-08-07 13:00"],
                        ["Entry Short", "2023-08-04 17:45"],
                        ["Exit Long", "2023-08-03 10:45"],
                        ["Entry Long", "2023-08-03 10:45"],
                    ],
                    columns=["Type", "Date/Time"],
                ),
                {
                    "strategy_id": 10,
                    "signals": [
                        {"signal_at": "2023-08-07T13:00+0700", "signal": {"S50": 0.0}},
                        {"signal_at": "2023-08-04T17:45+0700", "signal": {"S50": -0.5}},
                        {"signal_at": "2023-08-03T10:45+0700", "signal": {"S50": 0.0}},
                        {"signal_at": "2023-08-03T10:45+0700", "signal": {"S50": 0.5}},
                    ],
                },
            ),
            # case 2: The newest indication is holding.
            (
                pd.DataFrame(
                    data=[
                        ["Exit Short", np.nan],
                        ["Entry Short", "2023-08-04 17:45"],
                        ["Exit Long", "2023-08-03 10:45"],
                        ["Entry Long", "2023-08-03 10:45"],
                    ],
                    columns=["Type", "Date/Time"],
                ),
                {
                    "strategy_id": 10,
                    "signals": [
                        {"signal_at": "2023-08-04T17:45+0700", "signal": {"S50": -0.5}},
                        {"signal_at": "2023-08-03T10:45+0700", "signal": {"S50": 0.0}},
                        {"signal_at": "2023-08-03T10:45+0700", "signal": {"S50": 0.5}},
                    ],
                },
            ),
            # case 3: The daily signal format
            (
                pd.DataFrame(
                    data=[
                        ["Entry Short", "2023-08-04"],
                        ["Exit Long", "2023-08-03"],
                        ["Entry Long", "2023-08-03"],
                    ],
                    columns=["Type", "Date/Time"],
                ),
                {
                    "strategy_id": 10,
                    "signals": [
                        {"signal_at": "2023-08-04T00:00+0700", "signal": {"S50": -0.5}},
                        {"signal_at": "2023-08-03T00:00+0700", "signal": {"S50": 0.0}},
                        {"signal_at": "2023-08-03T00:00+0700", "signal": {"S50": 0.5}},
                    ],
                },
            ),
        ],
    )  # type: ignore
    def test_success_normal_case(self, df: pd.DataFrame, expect_result: dict):
        result = transform_list_of_trades(df=df, strategy_id=10, weight=0.5)
        # Check
        return assert_dict_equal(result, expect_result)


class TestFormatDatetime:
    @pytest.mark.parametrize(
        ("signal_list", "utc", "expect_result"),
        [
            # case 1: The daily format and UTC+7 (default)
            (
                [
                    {"signal_at": "2023-08-04", "signal": {}},
                    {"signal_at": "2023-08-03", "signal": {}},
                ],
                "UTC+7",
                [
                    {"signal_at": "2023-08-04T00:00+0700", "signal": {}},
                    {"signal_at": "2023-08-03T00:00+0700", "signal": {}},
                ],
            ),
            # case 2: Intra day format and UTC+8
            (
                [
                    {"signal_at": "2023-08-04 13:00", "signal": {}},
                    {"signal_at": "2023-08-04 14:00", "signal": {}},
                ],
                "UTC+8",
                [
                    {"signal_at": "2023-08-04T12:00+0700", "signal": {}},
                    {"signal_at": "2023-08-04T13:00+0700", "signal": {}},
                ],
            ),
            # case 3: Intra day format and UTC+0
            (
                [
                    {"signal_at": "2023-08-04 13:00", "signal": {}},
                    {"signal_at": "2023-08-04 14:00", "signal": {}},
                ],
                "UTC+0",
                [
                    {"signal_at": "2023-08-04T20:00+0700", "signal": {}},
                    {"signal_at": "2023-08-04T21:00+0700", "signal": {}},
                ],
            ),
            # case 3: Intra day format and UTC-5
            (
                [
                    {"signal_at": "2023-08-04 13:00", "signal": {}},
                    {"signal_at": "2023-08-04 14:00", "signal": {}},
                ],
                "UTC-5",
                [
                    {"signal_at": "2023-08-05T01:00+0700", "signal": {}},
                    {"signal_at": "2023-08-05T02:00+0700", "signal": {}},
                ],
            ),
        ],
    )
    def test_success_formate_datetime(
        self, signal_list: list[dict], utc: str, expect_result: list[dict]
    ):
        result = _format_datetime(signal_list=signal_list, utc=utc)
        assert [i for i in result if i not in expect_result] == []
