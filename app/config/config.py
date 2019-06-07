import os
import multiprocessing


def no_of_workers():
    return multiprocessing.cpu_count() * 2 + 1

class Config(object):
    APP_HOST = os.getenv('APP_HOST')
    APP_PORT = os.getenv('APP_PORT')
    TIMEOUT = os.getenv('TIMEOUT')
    TESSERACT_PATH = os.getenv('TESSERACT_PATH')
    WORKER_COUNT = no_of_workers()
    WORKER_CLASS = os.getenv('WORKER_CLASS')


app_config = Config()

