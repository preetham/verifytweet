import requests

from app.logger.logger import logger
from app.config.config import app_config


def search_results(entities):
    if not entities['date'] or not entities['user_id'] or not entities['tweet']:
        raise ValueError
    

