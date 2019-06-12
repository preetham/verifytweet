import requests

from urllib.parse import urljoin
from app.logger.logger import logger
from app.config.config import app_config


def search_results(querystring):
    if not querystring:
        return []
    headers = {'Authorization': 'Bearer ' + app_config.TWITTER_ACCESSTOKEN}
    search_url = urljoin(app_config.TWITTER_HOSTNAME + '/' +
                         app_config.TWITTER_APIVER + '/', app_config.TWITTER_CONTEXT)
    r = requests.get(search_url, headers=headers, params=querystring)
    response = r.json()
    logger.info('Response for Twitter API: ' + str(r.status_code))
    return response
