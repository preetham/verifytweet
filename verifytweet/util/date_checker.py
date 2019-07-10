# Verify Tweet verifies tweets of a public user
# from tweet screenshots: real or generated from
# tweet generators.
# Copyright (C) 2019 Preetham Kamidi

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime, timezone

from verifytweet.config.settings import app_config
from verifytweet.util.logging import logger


def valid_date(processed_date):
    """Check if processed date of tweet is older than configured duration

    Args:
        processed_date: Represents date of processed tweet from image.

    Returns:
        A Boolean indicating if tweet can be futher processed or not. 
    """
    if not processed_date or not isinstance(processed_date, datetime):
        return False
    curr_date = datetime.now(timezone.utc)
    datetime_diff = curr_date - processed_date
    if datetime_diff.days > 7:
        return False
    return True


def format_for_date(tweet_datetime: datetime):
    if not isinstance(tweet_datetime, datetime):
        raise TypeError('Tweet date has to be type datetime')
    if not tweet_datetime:
        raise ValueError('Tweet date has to be a valid datetime object')
    return tweet_datetime.strftime('%Y-%m-%d')
