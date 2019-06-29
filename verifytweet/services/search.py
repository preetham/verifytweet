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
import datetime
import twint
import urllib.parse as urlparser
import dateutil.parser as date_parser

import verifytweet.util.date_checker as date_checker

from verifytweet.util.logging import logger
from verifytweet.config.settings import app_config
from verifytweet.util.result import ResultStatus


class TwitterAPISearch(object):
    """Retrieve tweets of a user

    Retrieve tweets of a user tweeted on a single day
    using Twitter Search API.

    Attributes:
        user_id: A string denoting a twitter username.
        date: A datetime object representing the date in question.
    """

    def __init__(self, user_id: str, date: datetime.datetime):
        if not isinstance(user_id, str) or not isinstance(
                date, datetime.datetime):
            raise TypeError(
                'User ID must be type string and date must be type datetime.datetime'
            )
        if not user_id or not date:
            raise ValueError('User ID or Date cannot be empty')
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
        logger.info('Searching for tweet using Twitter API...')
        querystring = dict({
            app_config.TWEET_USERNAME_KEY: self.user_id,
            app_config.TWEET_COUNT_KEY: app_config.TWEET_COUNT
        })
        try:
            response, response_status = self._call_twitter_api(querystring)
            if response_status != ResultStatus.ALL_OKAY:
                return (None, response_status)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        same_day_tweets = list()
        for entry in response:
            tweet_date = date_parser.parse(entry[app_config.TWEET_DATE_KEY])
            if date_checker.format_for_date(
                    tweet_date) == date_checker.format_for_date(
                        self.date) and date_checker.valid_date(tweet_date):
                logger.info('Tweet found...: ' +
                            str(entry[app_config.TWEET_TEXT_KEY]))
                same_day_tweets.append(entry[app_config.TWEET_TEXT_KEY])
        if not same_day_tweets:
            return (same_day_tweets, ResultStatus.NO_RESULT)
        return (same_day_tweets, ResultStatus.ALL_OKAY)

    @staticmethod
    def _call_twitter_api(querystring):
        if not isinstance(querystring, dict):
            raise TypeError('Query String must be type dict')
        if not querystring:
            raise ValueError('Query String must be a valid dictionary')
        headers = {'Authorization': 'Bearer ' + app_config.TWITTER_ACCESSTOKEN}
        search_url = urlparser.urljoin(
            app_config.TWITTER_HOSTNAME + '/' + app_config.TWITTER_APIVER +
            '/', app_config.TWITTER_CONTEXT)
        r = requests.get(search_url, headers=headers, params=querystring)
        response = r.json()
        logger.info('Status Code for Twitter API: ' + str(r.status_code))
        if r.status_code != 200:
            raise RuntimeError('Twitter API returned status:' +
                               str(r.status_code))
        if not response:
            return (response, ResultStatus.NO_RESULT)
        return (response, ResultStatus.ALL_OKAY)


class TwintSearch(object):
    """Search using Twint
    """

    def __init__(self, user_id: str, date: datetime.datetime,
                 tweet_snippet: str):
        if not isinstance(user_id, str) or not isinstance(
                date, datetime.datetime) or not (tweet_snippet, str):
            raise TypeError(
                'User ID and tweet_snippet must be type string, date must be type datetime.datetime'
            )
        if not user_id or not date or not tweet_snippet:
            raise ValueError('User ID, Tweet or Date cannot be empty')
        self.user_id = user_id
        self.date = date
        self.tweet_snippet = tweet_snippet

    def search(self):
        twint_config = twint.Config()
        twint_config.Username = self.user_id
        twint_config.Search = self.tweet_snippet
        twint_config.Since = date_checker.format_for_date(self.date)
        twint_config.Limit = app_config.TWEET_MAX_STORE
        twint_config.Store_object = True
        try:
            twint.run.Search(twint_config)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        results = twint.output.tweets_object
        if not results:
            return (results, ResultStatus.NO_RESULT)
        logger.info(f'Search results: {results}\n')
        return (results, ResultStatus.ALL_OKAY)
