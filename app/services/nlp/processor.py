from re import findall, search

from app.logger.logger import logger


def get_entities(text: str):
    if not text:
        return {}
    user_id = findall(r'@(\w{1,15})\b', text)
    datetime = search(r'\d{1,2}\s\w+\s\d{4}', text).group()
    return {
        'user_id': user_id,
        'tweet': 'TBB',
        'datetime': datetime
    }
    
