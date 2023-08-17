import logging
import logging.config

from finnizeclient.client.upload_signal import upload_backtest_signals
from finnizeclient.utils import read_list_of_trades, transform_list_of_trades

# Get the logger instance
logger = logging.getLogger(__name__)


def upload_tradingview_signal(
    path: str,
    strategy_id: int,
    weight: float,
    utc="UTC+7",
    url="https://client-gateway.finnize.com/api/v1/strategy-signal/",
):
    """Uploads trading signals generated from a TradingView exported CSV file to the
    Finnize website.

    This function reads a CSV file containing trade data exported from TradingView, transforms
    the data into a signal dictionary format, and uploads the signals to the Finnize website.

    Parameters
    ----------
    path : str
        The file path to the CSV file containing trading data exported from TradingView.
    strategy_id : int
        The unique identifier for the trading strategy associated with the signals.
    weight : float
        A weight or significance factor associated with the signals.
    utc : str, optional
        The UTC offset in the format 'UTC±X', where X is the offset in hours. Default is 'UTC+7'.
    url : str, optional
        The URL endpoint where the signals will be uploaded, by default "https://client-gateway.finnize.com/api/v1/strategy-signal/"

    Note
    -----
    - DEV endpoint: https://dev-client-gateway.finnize.com/api/v1/strategy-signal/
    - UAT endpoint: https://uat-client-gateway.finnize.com/api/v1/strategy-signal/
    - PRD endpoint: https://client-gateway.finnize.com/api/v1/strategy-signal/
    """
    # read CSV files
    df = read_list_of_trades(path=path)

    # transform CSV files to signal dictionary before sent to Finnize website
    strategy_signal = transform_list_of_trades(
        df=df, strategy_id=strategy_id, weight=weight, utc=utc
    )
    logger.debug("Transform signal successful")

    # upload to finnize website
    upload_backtest_signals(strategy_signal=strategy_signal, url=url)
    logger.debug("Upload successful")
