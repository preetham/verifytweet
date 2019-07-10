# Verify Tweet verifies tweets of a public user
# from tweet screenshots: real or generated from
# tweet generators.
# Copyright (C) 2019 Preetham Kamidi

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import datetime
import string
import random
import nltk
import dateutil.parser as date_parser

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from verifytweet.util.logging import logger
from verifytweet.config.settings import app_config
from verifytweet.util.result import ResultStatus

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
count_vectorizer = CountVectorizer()
stopwords = set(nltk.corpus.stopwords.words('english'))

USERNAME_REGEX = r'@(\w{1,15})\b'
DATETIME_REGEX = r'((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))\s-\s\d{1,2}\s\w+\s\d{4}'
ALPHANUM_REGEX = r'[^A-Za-z0-9]+'


class DataParser(object):
    """Parses data from extracted text
    """

    def __init__(self):
        pass

    def get_entities(self, extracted_text: str):
        """Parses entities from extracted text.

        Parses username (denoted by user_id), tweet as well as date from extracted text.

        Attributes:
            extracted_text: A string denoting extracted text from image.

        Returns:
            A tuple contaning a dictionary: a mapping of user_id, tweet and date
            as well as Enum ResultStatus which gives out result status.
            For example: ::

                {
                    "user_id": "elonmusk",
                    "tweet": "Ms. Tree caught the Falcon fairing!!",
                    "date": datetime.datetime(2019, 6, 8, 7, 29, tzinfo=datetime.timezone.utc)
                }

        """
        if not isinstance(extracted_text, str):
            raise TypeError('Extracted text must be type string')
        if not extracted_text:
            raise ValueError('Extracted text cannot be empty')
        logger.info('Parsing data out of extracted text...')
        username_match = re.search(USERNAME_REGEX, extracted_text)
        datetime_match = re.search(DATETIME_REGEX, extracted_text)
        if not username_match:
            return (dict({
                'user_id': None,
                'tweet': None,
                'datetime': None
            }), ResultStatus.NO_RESULT)
        user_id = username_match.group()[1:]
        tweet_start_index = username_match.end()
        tweet_end_index = len(
            extracted_text
        ) - 1 if not datetime_match else datetime_match.start()
        tweet = extracted_text[tweet_start_index:tweet_end_index].strip()
        if not datetime_match:
            return (dict({
                'user_id': user_id,
                'tweet': tweet,
                'date': None
            }), ResultStatus.ALL_OKAY)
        date_str = datetime_match.group().replace('-', '')
        processed_datetime = date_parser.parse(date_str).replace(
            tzinfo=datetime.timezone.utc)
        return (dict({
            'user_id': user_id,
            'tweet': tweet,
            'date': processed_datetime
        }), ResultStatus.ALL_OKAY)

    def clean_text(self, extracted_text: str):
        """Removes stop words and samples words out of tweet
        to create a snippet.

        Attributes:
            extracted_text: A string denoting extracted text from image.

        Returns:
            A tuple contaning a tweet snippet
            as well as Enum ResultStatus which gives out result status.
        """
        if not isinstance(extracted_text, str):
            raise TypeError('Extracted text must be type string')
        if not extracted_text:
            raise ValueError('Extracted text cannot be empty')
        try:
            non_punc_tweet = extracted_text.translate(
                str.maketrans('', '', string.punctuation))
            word_tokens = nltk.tokenize.word_tokenize(non_punc_tweet)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        filtered_sentence = [w for w in word_tokens if not w in stopwords]
        picked_words = filtered_sentence[2:min([len(filtered_sentence), 6])]
        tweet_snippet = " ".join(picked_words)
        if not tweet_snippet:
            return (tweet_snippet, ResultStatus.NO_RESULT)
        logger.debug(f'Tweet Snippet: {tweet_snippet}')
        return (tweet_snippet, ResultStatus.ALL_OKAY)


class TextProcessor(object):
    """Processes extracted tweet and aggregated tweets
    """

    def __init__(self):
        pass

    def get_similarity(self, extracted_tweet: str, same_day_tweets: list):
        """Calculates a similarity matrix.

        Calculates a similarity matrix of the corpus containing
        extracted tweet and tweets aggregated from Twitter Search API
        using consine similarity approach.

        Attributes:
            extracted_tweet: A string denoting extracted tweet from image.
            same_day_tweets: A list contaning tweets of target date

        Returns:
            A tuple contaning a similarity matrix, which is a numpy array
            as well as Enum ResultStatus which gives out result status.
            For example: ::

                ([[1.        0.9258201]
                 [0.9258201 1.       ]], ResultStatus.ALL_OKAY)


        """
        if not isinstance(extracted_tweet, str) or not isinstance(
                same_day_tweets, list):
            raise TypeError(
                'Extracted tweet must be type str and Same day tweets must be type list'
            )
        if not extracted_tweet or not same_day_tweets:
            raise ValueError(
                'Extracted tweet must be a valid string and same day tweets must be a valid list'
            )
        logger.info('Processing similarity of two tweets...')
        corpus = list()
        corpus.append(extracted_tweet)
        corpus.extend(same_day_tweets)
        logger.debug('Corpus: ' + str(corpus))
        try:
            sparse_matrix = count_vectorizer.fit_transform(corpus)
            similarity_matrix = cosine_similarity(sparse_matrix, sparse_matrix)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        logger.debug('Similartiy Matrix: ' + str(similarity_matrix))
        return (similarity_matrix, ResultStatus.ALL_OKAY)
