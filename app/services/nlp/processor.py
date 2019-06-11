from re import search
from dateutil.parser import parse


from app.logger.logger import logger


def get_entities(text: str):
    if not text:
        return {}
    username_match = search(r'@(\w{1,15})\b', text)
    date_match = search(r'\d{1,2}\s\w+\s\d{4}', text)
    if not username_match or not date_match:
        return {
            'user_id': None,
            'tweet': None,
            'datetime': None
        }
    user_id = username_match.group()
    date_str = date_match.group()
    date = parse(date_str)
    formatted_date = date.strftime('%Y-%m-%d')
    username_end_index = username_match.end()
    date_start_index = date_match.start()
    tweet = text[username_end_index+5:date_start_index-10]
    return {
        'user_id': user_id,
        'tweet': tweet,
        'date': formatted_date
    }
    
