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

import verifytweet.services.image as image_service
import verifytweet.services.text as text_service
import verifytweet.services.search as search_service
import verifytweet.util.date_checker as date_checker
import verifytweet.util.validator as validator

from verifytweet.util.logging import logger
from verifytweet.config.settings import app_config
from verifytweet.util.result import ResultStatus


class APIApproach(object):
    """Use Twitter API to verify tweet

    Attributes:
        file_path: A string denoting a twitter username.
    """

    def __init__(self, file_path: str):
        if not isinstance(file_path, str):
            raise TypeError('File path must be type str')
        if not file_path:
            raise ValueError('File path must be a valid string')
        self.file_path = file_path

    def exec(self):
        """Executes controller flow

        Controller uses image service to extract text from
        image, passes text to text service to parse entities such
        as username, tweet as well as date, uses search service 
        to retrieve same day tweets, text service to find similar tweet
        and finally verifying the tweet.

        Returns:
            valid_tweet: A tweet object
            status: Enum ResultStatus representing result status

        """
        entities, preprocess_status = preprocess(self.file_path)
        if preprocess_status != ResultStatus.ALL_OKAY:
            return (None, ResultStatus.MODULE_FAILURE)

        try:
            search_controller = search_service.TwitterAPISearch(
                entities['user_id'], entities['date'])
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        same_day_tweets, search_status = search_controller.aggregate_tweets()
        if search_status != ResultStatus.ALL_OKAY:
            return (None, search_status)

        try:
            text_processor = text_service.TextProcessor(
                entities['tweet'], same_day_tweets)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        similarity_matrix, processor_status = text_processor.get_similarity()
        if processor_status != ResultStatus.ALL_OKAY:
            return (None, processor_status)

        try:
            valid_tweet, validator_status = validator.verify_validity(
                similarity_matrix)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        if validator_status != ResultStatus.ALL_OKAY:
            return (None, validator_status)
        logger.info('Tweet Validity: ' + str(valid_tweet))
        return (valid_tweet, ResultStatus.ALL_OKAY)


class NonAPIApproach(object):
    """Use a non-api approach to verify tweet

    Attributes:
        file_path: A string denoting a twitter username.
    """

    def __init__(self, file_path: str):
        if not isinstance(file_path, str):
            raise TypeError('File path must be type str')
        if not file_path:
            raise ValueError('File path must be a valid string')
        self.file_path = file_path

    def exec(self):
        """Executes controller flow

        Controller uses image service to extract text from
        image, passes text to text service to parse entities such
        as username, tweet as well as date, uses search service 
        to retrieve a tweet if available.

        Returns:
            search_results: list of tweet objects
            status: Enum ResultStatus representing result status

        """
        entities, preprocess_status = preprocess(self.file_path)
        if preprocess_status != ResultStatus.ALL_OKAY:
            return (None, ResultStatus.MODULE_FAILURE)

        try:
            text_processor = text_service.DataParser(entities['tweet'])
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        tweet_snippet, text_processor_status = text_processor.clean_text()
        if text_processor_status != ResultStatus.ALL_OKAY:
            return (None, text_processor_status)

        try:
            search_controller = search_service.TwintSearch()
            search_results, search_status = search_controller.search(
                entities['user_id'], entities['date'], tweet_snippet)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)
        if search_status != ResultStatus.ALL_OKAY:
            return (None, search_status)

        return (search_results[0], ResultStatus.ALL_OKAY)


def preprocess(file_path):
    """Preprocesses text

    Extracts text from image using image service,
    parses entities from text using text service.

    Args:
        file_path: represents path of the image file.

    Returns:
        entities: Entities parsed from text such as tweet, user_id and date.
        status: Enum ResultStatus representing result status

    """
    try:
        text_extractor = image_service.Extractor(file_path)
    except Exception as e:
        logger.exception(e)
        return (None, ResultStatus.MODULE_FAILURE)
    extracted_text, extractor_status = text_extractor.get_text()
    if extractor_status != ResultStatus.ALL_OKAY:
        return (None, extractor_status)
    logger.debug('Processed text: ' + extracted_text)

    try:
        entity_parser = text_service.DataParser(extracted_text)
    except Exception as e:
        logger.exception(e)
        return (None, ResultStatus.MODULE_FAILURE)
    entities, parser_status = entity_parser.get_entities()
    if parser_status != ResultStatus.ALL_OKAY:
        return (None, parser_status)
    logger.debug('Entities: ' + str(entities))
    return (entities, parser_status)
