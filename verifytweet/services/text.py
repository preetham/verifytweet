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


class DataParser(object):
    """Parses data from extracted text

    Attributes:
        extracted_text: A string denoting extracted text from image.
    """

    def __init__(self, extracted_text: str):
        if not isinstance(extracted_text, str):
            raise TypeError('Extracted text must be type string')
        if not extracted_text:
            raise ValueError('Extracted text cannot be empty')
        self.text = extracted_text

    def get_entities(self):
        """Parses entities from extracted text.

        Parses username (denoted by user_id), tweet as well as date from extracted text.

        Args:
            self: represents instance of DataParser class

        Returns:
            A dictionary contaning a mapping of user_id, tweet and date.
            For example:

            {
                "user_id": "elonmusk",
                "tweet": "Ms. Tree caught the Falcon fairing!!",
                "date": datetime.datetime(2019, 6, 8, 7, 29, tzinfo=datetime.timezone.utc)
            }
        """
        logger.info('Parsing data out of extracted text...')
        username_match = re.search(r'@(\w{1,15})\b', self.text)
        datetime_match = re.search(
            r'((1[0-2]|0?[1-9]):([0-5][0-9]) ?([AaPp][Mm]))\s-\s\d{1,2}\s\w+\s\d{4}',
            self.text)
        if not username_match or not datetime_match:
            return (dict({
                'user_id': None,
                'tweet': None,
                'datetime': None
            }), ResultStatus.NO_RESULT)
        user_id = username_match.group()[1:]
        date_str = datetime_match.group().replace('-', '')
        processed_datetime = date_parser.parse(date_str).replace(
            tzinfo=datetime.timezone.utc)
        username_end_index = username_match.end()
        date_start_index = datetime_match.start()
        tweet = self.text[username_end_index + 5:date_start_index].strip()
        return (dict({
            'user_id': user_id,
            'tweet': tweet,
            'date': processed_datetime
        }), ResultStatus.ALL_OKAY)

    def clean_text(self):
        """Remove stop words and randomly sample words out of tweet
        """
        try:
            non_punc_tweet = self.text.translate(
                str.maketrans('', '', string.punctuation))
            word_tokens = nltk.tokenize.word_tokenize(non_punc_tweet)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        filtered_sentence = [w for w in word_tokens if not w in stopwords]
        picked_words = filtered_sentence[0:min([len(filtered_sentence), 4])]
        tweet_snippet = " ".join(picked_words)
        if not tweet_snippet:
            return (tweet_snippet, ResultStatus.NO_RESULT)
        logger.info(f'Tweet Snippet: {tweet_snippet}')
        return (tweet_snippet, ResultStatus.ALL_OKAY)


class TextProcessor(object):
    """Processes extracted tweet and aggregated tweets

    Attributes:
        extracted_tweet: A string denoting extracted tweet from image.
        same_day_tweets: A list contaning tweets of target date
    """

    def __init__(self, extracted_tweet: str, same_day_tweets: list):
        if not isinstance(extracted_tweet, str) or not isinstance(
                same_day_tweets, list):
            raise TypeError(
                'Extracted tweet must be type str and Same day tweets must be type list'
            )
        if not extracted_tweet or not same_day_tweets:
            raise ValueError(
                'Extracted tweet must be a valid string and same day tweets must be a valid list'
            )
        self.extracted_tweet = extracted_tweet
        self.same_day_tweets = same_day_tweets

    def get_similarity(self):
        """Calculates a similarity matrix.

        Calculates a similarity matrix of the corpus containing
        extracted tweet and tweets aggregated from Twitter Search API
        using consine similarity approach.

        Args:
            self: represents instance of TextProcessor class

        Returns:
            A similarity matrix.
            For example:
            [[1.        0.9258201]
             [0.9258201 1.       ]]
        """
        logger.info('Processing similarity of two tweets...')
        corpus = list()
        corpus.append(self.extracted_tweet)
        corpus.extend(self.same_day_tweets)
        logger.info('Corpus: ' + str(corpus))
        try:
            sparse_matrix = count_vectorizer.fit_transform(corpus)
            similarity_matrix = cosine_similarity(sparse_matrix, sparse_matrix)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        logger.info('Similartiy Matrix: ' + str(similarity_matrix))
        return (similarity_matrix, ResultStatus.ALL_OKAY)
