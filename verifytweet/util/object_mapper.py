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

from twint.tweet import tweet
from verifytweet.config.settings import app_config
from verifytweet.util.logging import logger
from verifytweet.util.result import ResultStatus

def map_keys(tweet_obj):
    """Map members of tweet object to a dictionary.

    Args:
        tweet_obj: Represents a tweet object.

    Returns:
        A dictionary contaning a mapping of members of tweet object 
    """
    if not isinstance(tweet_obj, tweet):
        raise TypeError('Tweet object must be of type twint.tweet')
    try:
        id = tweet_obj.id
    except AttributeError:
        raise ValueError('Tweet object must be valid')
    return (dict({
        "id": tweet_obj.id,
        "conversation_id": tweet_obj.conversation_id,
        "datetime": tweet_obj.datetime,
        "datestamp":tweet_obj.datestamp,
        "timestamp":tweet_obj.timestamp,
        "user_id":tweet_obj.user_id,
        "username":tweet_obj.username,
        "name":tweet_obj.name,
        "place":tweet_obj.place,
        "timezone":tweet_obj.timezone,
        "mentions":tweet_obj.mentions,
        "urls":tweet_obj.urls,
        "photos":tweet_obj.photos,
        "video":tweet_obj.video,
        "tweet":tweet_obj.tweet,
        "hashtags":tweet_obj.hashtags,
        "replies_count":tweet_obj.replies_count,
        "retweets_count":tweet_obj.retweets_count,
        "likes_count":tweet_obj.likes_count,
        "link":tweet_obj.link,
        "retweet":tweet_obj.retweet
    }), ResultStatus.ALL_OKAY)
