import logging
import logging.config
import traceback

from src.client.upload_signal import upload_backtest_signals
from src.utils import read_list_of_trades, transform_list_of_trades

# Get the logger instance
logger = logging.getLogger(__name__)


def upload_tradingview_signal(path: str, strategy_id: int, weight: float, url: str):
    try:
        # read CSV files
        df = read_list_of_trades(path=path)

        # transform CSV files to signal dictionary before sent to Finnize website
        strategy_signal = transform_list_of_trades(df=df, strategy_id=strategy_id, weight=weight)
        logger.debug("Transform signal successful")

        # upload to finnize website
        upload_backtest_signals(strategy_signal=strategy_signal, url=url)
        logger.debug("Upload successful")
    except Exception:
        logger.error(traceback.format_exc())
