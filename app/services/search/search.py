import requests

from urllib.parse import urljoin
from app.logger.logger import logger
from app.config.config import app_config


def search_results(entities):
    if not entities['date'] or not entities['user_id'] or not entities['tweet']:
        raise ValueError
    headers = {'Authorization': 'Bearer ' + app_config.TWITTER_ACCESSTOKEN}
    querystring = {'screen_name': entities['user_id'] , 'count': app_config.TWEET_COUNT}
    search_url = urljoin(app_config.TWITTER_HOSTNAME + '/' +
                         app_config.TWITTER_APIVER + '/', app_config.TWITTER_CONTEXT)
    r = requests.get(search_url, headers=headers, querystring=querystring)
    response = r.json()
    return response['statuses']
