from dateutil.parser import parse


from app.logger.logger import logger
from app.config.config import app_config
from app.util.date_checker import valid, format_for_date
from app.services.search import search


def search_controller(entities):
    if not entities or not entities['user_id']:
        return {}
    logger.info('Searching for tweet using Twitter API...')
    querystring = {
        app_config.TWEET_USERNAME_KEY: entities['user_id'], app_config.TWEET_COUNT_KEY: app_config.TWEET_COUNT}
    response = search.search_results(querystring)
    same_day_tweets = list()
    for entry in response:
        tweet_date = parse(entry[app_config.TWEET_DATE_KEY])
        if format_for_date(tweet_date) == format_for_date(entities['date']) and valid(tweet_date):
            logger.info('Tweet found...: ' + str(entry[app_config.TWEET_TEXT_KEY]))
            same_day_tweets.append(entry[app_config.TWEET_TEXT_KEY])
    return same_day_tweets
