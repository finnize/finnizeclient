import numpy as np
import pandas as pd
import pytest
from pandas._testing import assert_dict_equal
from pandas.testing import assert_frame_equal

from src.utils import transform_list_of_trades


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
                        {"signal_at": "2023-08-07 13:00", "signal": {"S50": 0.0}},
                        {"signal_at": "2023-08-04 17:45", "signal": {"S50": -0.5}},
                        {"signal_at": "2023-08-03 10:45", "signal": {"S50": 0.0}},
                        {"signal_at": "2023-08-03 10:45", "signal": {"S50": 0.5}},
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
                        {"signal_at": "2023-08-04 17:45", "signal": {"S50": -0.5}},
                        {"signal_at": "2023-08-03 10:45", "signal": {"S50": 0.0}},
                        {"signal_at": "2023-08-03 10:45", "signal": {"S50": 0.5}},
                    ],
                },
            ),
        ],
    )
    def test_success_normal_case(self, df: pd.DataFrame, expect_result: dict):
        result = transform_list_of_trades(df=df, strategy_id=10, weight=0.5)

        # Check
        return assert_dict_equal(result, expect_result)
