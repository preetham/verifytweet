from datetime import datetime, timezone

from app.config.config import app_config
from app.logger.logger import logger


def valid(processed_date):
    if not processed_date:
        return False
    curr_date = datetime.now(timezone.utc)
    datetime_diff = curr_date - processed_date
    if datetime_diff.days > app_config.TWEET_MAX_OLD:
        return False
    return True

def format_for_date(tweet_datetime:datetime):
    return tweet_datetime.strftime('%Y-%m-%d')
