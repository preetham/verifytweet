from re import search
from datetime import timezone
from dateutil.parser import parse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.logger.logger import logger
from app.config.config import app_config


count_vectorizer = CountVectorizer()

def get_entities(text: str):
    if not text:
        return {}
    logger.info('Parsing data out of processed text...')
    username_match = search(r'@(\w{1,15})\b', text)
    datetime_match = search(
        r'((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))\s-\s\d{1,2}\s\w+\s\d{4}', text)
    if not username_match or not datetime_match:
        return {
            'user_id': None,
            'tweet': None,
            'datetime': None
        }
    user_id = username_match.group()[1:]
    date_str = datetime_match.group().replace('-', '')
    processed_datetime = parse(date_str).replace(tzinfo=timezone.utc)
    username_end_index = username_match.end()
    date_start_index = datetime_match.start()
    tweet = text[username_end_index+5:date_start_index].strip()
    return {
        'user_id': user_id,
        'tweet': tweet,
        'date': processed_datetime
    }
    

def get_similarity(processed_tweet:str, same_day_tweets:list):
    if not processed_tweet or not same_day_tweets:
        return []
    logger.info('Processing similarity of two tweets...')
    corpus = list()
    corpus.append(processed_tweet)
    corpus.extend(same_day_tweets)
    logger.info('Corpus: ' + str(corpus))
    sparse_matrix = count_vectorizer.fit_transform(corpus)
    similarity_matrix = cosine_similarity(sparse_matrix, sparse_matrix)
    print(similarity_matrix)
    for row in similarity_matrix:
        for column in row:
            if column > app_config.SIMILARITY_THRESHOLD:
                return True
    return False
