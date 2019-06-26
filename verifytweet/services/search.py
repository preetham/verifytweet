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


import requests
import urllib.parse as urlparser
import dateutil.parser as date_parser

import verifytweet.shared.date_checker as date_checker

from verifytweet.shared.logging import logger
from verifytweet.config.settings import app_config


class SearchController(object):
    """Retrieve tweets of a user

    Retrieve tweets of a user tweeted on a single day
    using Twitter Search API.

    Attributes:
        user_id: A string denoting a twitter username.
        date: A datetime object representing the date in question.
    """

    def __init__(self, user_id:str, date):
        self.user_id = user_id
        self.date = date

    def aggregate_tweets(self):
        """Aggregates tweets from a single day.

        Retrieves tweets pertaining to the given username and date using Twitter Search API.
        Aggregates tweets to a list.

        Args:
            self: represents instance of the SearchController class

        Returns:
            A list contaning a dict representing a Tweet Object. 
            Ref: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.
            For example:

            {"created_at": "Wed Oct 10 20:19:24 +0000 2018",
             "text": "To make room for more expression, 
                we will now count all emojis as equal—including
                those with gender‍‍‍ ‍‍and skin t… https://t.co/MkGjXf9aXm"
            }
        """
        if not self.user_id or not self.date:
            return list()
        logger.info('Searching for tweet using Twitter API...')
        querystring = {
            app_config.TWEET_USERNAME_KEY: self.user_id,
            app_config.TWEET_COUNT_KEY: app_config.TWEET_COUNT
        }
        response = self._call_twitter_api(querystring)
        same_day_tweets = list()
        for entry in response:
            tweet_date = date_parser.parse(entry[app_config.TWEET_DATE_KEY])
            if date_checker.format_for_date(tweet_date) == date_checker.format_for_date(
                    self.date) and date_checker.valid_date(tweet_date):
                logger.info('Tweet found...: ' +
                            str(entry[app_config.TWEET_TEXT_KEY]))
                same_day_tweets.append(entry[app_config.TWEET_TEXT_KEY])
        return same_day_tweets

    @staticmethod
    def _call_twitter_api(querystring):
        if not querystring:
            return list()
        headers = {'Authorization': 'Bearer ' + app_config.TWITTER_ACCESSTOKEN}
        search_url = urlparser.urljoin(
            app_config.TWITTER_HOSTNAME + '/' + app_config.TWITTER_APIVER + '/',
            app_config.TWITTER_CONTEXT)
        r = requests.get(search_url, headers=headers, params=querystring)
        response = r.json()
        logger.info('Response for Twitter API: ' + str(r.status_code))
        if r.status_code != 200:
            return list()
        return response
