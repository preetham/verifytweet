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

    def __init__(self):
        pass

    def aggregate_tweets(self, user_id: str, date: datetime.datetime):
        """Aggregates tweets from a single day.

        Retrieves tweets pertaining to the given username and date using Twitter Search API.
        Aggregates tweets to a list.

        Returns:
            A list contaning a dict representing a Tweet Object. 
            
            Ref: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.
            
            For example: ::

                {
                    "created_at": "Wed Oct 10 20:19:24 +0000 2018",
                    "text": "To make room for more expression, we will now count all emojis as equal—including those with gender‍‍‍ ‍‍and skin t… https://t.co/MkGjXf9aXm"
                }

        """
        if not isinstance(user_id, str) or not isinstance(
                date, datetime.datetime):
            raise TypeError(
                'User ID must be type string and date must be type datetime.datetime'
            )
        if not user_id or not date:
            raise ValueError('User ID or Date cannot be empty')
        logger.info('Searching for tweet using Twitter API...')
        querystring = dict({
            app_config.TWEET_USERNAME_KEY: user_id,
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
                        date) and date_checker.valid_date(tweet_date):
                logger.debug('Tweet found...: ' +
                             str(entry[app_config.TWEET_TEXT_KEY]))
                same_day_tweets.append(entry)
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
        logger.debug('Status Code for Twitter API: ' + str(r.status_code))
        if r.status_code != 200:
            raise RuntimeError('Twitter API returned status:' +
                               str(r.status_code))
        if not response:
            return (response, ResultStatus.NO_RESULT)
        return (response, ResultStatus.ALL_OKAY)


class TwintSearch(object):
    """Search for tweets using Twint

    Retrieves tweets of a user using twint basing on
    username, date as well as tweet snippet.

    Attributes:
        user_id: A string denoting a twitter username.
        date: A datetime object representing the date in question.
        tweet_snippet: A snippet of tweet extracted from image.
    """

    def __init__(self):
        pass

    def search(self, user_id: str, tweet_snippet: str,
               date: datetime.datetime = None):
        """Searches for tweets

        Retrieves tweets of given username, date as well as tweet snippet using Twint.
        Aggregates tweets to a list.

        Returns:
            A tuple contaning a list of results, each result represents a tweet object
            as well as ResultStatus.
            For example: ::

                ([<tweet_obj>], ResultStatus.ALL_OKAY)

        """
        if not isinstance(user_id, str) or not (tweet_snippet, str):
            raise TypeError(
                'User ID and tweet_snippet must be type string, date must be type datetime.datetime'
            )
        if not user_id or not tweet_snippet:
            raise ValueError('User ID, Tweet or Date cannot be empty')
        results = list()
        twint_config = twint.Config()
        twint_config.Username = user_id
        if date:
            twint_config.Since = date_checker.format_for_date(date)
            twint_config.Until = date_checker.format_for_date(date + datetime.timedelta(days=2))
        else:
            twint_config.Search = tweet_snippet
        twint_config.Limit = app_config.TWEET_MAX_STORE
        twint_config.Store_object = True
        twint_config.Store_object_tweets_list = results
        try:
            twint.run.Search(twint_config)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        if not results:
            return (results, ResultStatus.NO_RESULT)
        logger.debug(f'Search results: {results}\n')
        return (results, ResultStatus.ALL_OKAY)
