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

import os
import multiprocessing
import tempfile
import logging


def no_of_workers():
    """Returns no.of workers to be spawned

    Retrieves cpu count using multiprocessing module.
    No.of workers suggested is one more than 
    twice the cpu count.

    """
    return multiprocessing.cpu_count() * 2 + 1


class Config(object):
    """Configuration for the app
    """

    IMAGEMAGICK_PATH = os.getenv('IMAGEMAGICK_PATH') if os.getenv(
        'IMAGEMAGICK_PATH') else "convert"
    FILE_DIRECTORY = tempfile.mkdtemp()
    TWEET_MAX_STORE = 150
    RUN_METHOD = "cli"
    LOG_LEVEL = logging.DEBUG if os.getenv('VERIFYTWEET_DEBUG') else logging.INFO
    ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
    SIMILARITY_THRESHOLD = 0.6


class TwitterAPIConfig(Config):
    """Twitter API Configuration
    """

    TWITTER_ACCESSTOKEN = os.getenv('TWITTER_ACCESSTOKEN')
    TWITTER_HOSTNAME = "https://api.twitter.com"
    TWITTER_APIVER = "1.1"
    TWITTER_CONTEXT = "statuses/user_timeline.json"
    TWEET_DATE_KEY = "created_at"
    TWEET_USERNAME_KEY = "screen_name"
    TWEET_COUNT = 150
    TWEET_COUNT_KEY = "count"
    TWEET_MAX_OLD = 7
    TWEET_TEXT_KEY = "text"


class WebConfig(Config):
    """Configuration for running as web service
    """

    APP_HOST = os.getenv('APP_HOST') or '0.0.0.0'
    APP_PORT = os.getenv('APP_PORT') or '8000'
    TIMEOUT = 2000
    MAX_CONTENT_LENGTH_KEY = "MAX_CONTENT_LENGTH"
    MAX_CONTENT_LENGTH = 2097152
    WORKER_COUNT = no_of_workers()
    WORKER_CLASS = "eventlet"


run_method = "web" if "VERIFYTWEET_RUN_FOR_WEB" in os.environ else "cli"
Config.RUN_METHOD = run_method
configurations = dict({
    "cli": Config,
    "web": WebConfig,
})

app_config = configurations[run_method]
