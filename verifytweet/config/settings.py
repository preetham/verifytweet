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

    APP_HOST = os.getenv('APP_HOST')
    APP_PORT = os.getenv('APP_PORT')
    TIMEOUT = os.getenv('TIMEOUT')
    MAX_CONTENT_LENGTH_KEY = os.getenv('MAX_CONTENT_LENGTH_KEY')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH'))
    TESSERACT_PATH = os.getenv('TESSERACT_PATH')
    IMAGEMAGICK_PATH = os.getenv('IMAGEMAGICK_PATH')
    UPSCALE_RESOLUTION = os.getenv('UPSCALE_RESOLUTION')
    WORKER_COUNT = no_of_workers()
    WORKER_CLASS = os.getenv('WORKER_CLASS')
    FILE_DIRECTORY = os.getenv('FILE_DIRECTORY')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS').split(','))
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD'))
    TWITTER_HOSTNAME = os.getenv('TWITTER_HOSTNAME')
    TWITTER_APIVER = os.getenv('TWITTER_APIVER')
    TWITTER_CONTEXT = os.getenv('TWITTER_CONTEXT')
    TWITTER_ACCESSTOKEN = os.getenv('TWITTER_ACCESSTOKEN')
    TWEET_COUNT = int(os.getenv('TWEET_COUNT'))
    TWEET_DATE_KEY = os.getenv('TWEET_DATE_KEY')
    TWEET_USERNAME_KEY = os.getenv('TWEET_USERNAME_KEY')
    TWEET_COUNT_KEY = os.getenv('TWEET_COUNT_KEY')
    TWEET_MAX_OLD = int(os.getenv('TWEET_MAX_OLD'))
    TWEET_TEXT_KEY = os.getenv('TWEET_TEXT_KEY')

app_config = Config()
