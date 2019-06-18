import os
import multiprocessing


def no_of_workers():
    return multiprocessing.cpu_count() * 2 + 1

class Config(object):
    APP_HOST = os.getenv('APP_HOST')
    APP_PORT = os.getenv('APP_PORT')
    TIMEOUT = os.getenv('TIMEOUT')
    MAX_CONTENT_LENGTH = os.getenv('MAX_CONTENT_LENGTH')
    TESSERACT_PATH = os.getenv('TESSERACT_PATH')
    IMAGEMAGICK_PATH = os.getenv('IMAGEMAGICK_PATH')
    UPSCALE_PERCENTAGE = os.getenv('UPSCALE_PERCENTAGE')
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

