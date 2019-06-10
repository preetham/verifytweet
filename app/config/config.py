import os
import multiprocessing


def no_of_workers():
    return multiprocessing.cpu_count() * 2 + 1

class Config(object):
    APP_HOST = os.getenv('APP_HOST')
    APP_PORT = os.getenv('APP_PORT')
    TIMEOUT = os.getenv('TIMEOUT')
    TESSERACT_PATH = os.getenv('TESSERACT_PATH')
    IMAGEMAGICK_PATH = os.getenv('IMAGEMAGICK_PATH')
    UPSCALE_PERCENTAGE = os.getenv('UPSCALE_PERCENTAGE')
    WORKER_COUNT = no_of_workers()
    WORKER_CLASS = os.getenv('WORKER_CLASS')
    FILE_DIRECTORY = os.getenv('FILE_DIRECTORY')
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS').split(','))
    TWITTER_HOSTNAME = os.getenv('TWITTER_HOSTNAME')


app_config = Config()

