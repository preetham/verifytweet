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

from verifytweet.util.logging import logger
from verifytweet.util.result import ResultStatus


def extract_and_parse(file_path: str):
    """Preprocess text from image

    Extracts text from image using image service,
    parses entities from text using text service.

    Args:
        file_path: represents path of the image file.

    Returns:
        entities: Entities parsed from text such as tweet, user_id and date.
        status: Enum ResultStatus representing result status

    """
    if not isinstance(file_path, str):
            raise TypeError('File path must be type string')
    if not file_path:
        raise ValueError('File path must be a valid path')
    try:
        text_extractor = image_service.Extractor()
        extracted_text, extractor_status = text_extractor.get_text(file_path)
    except Exception as e:
        logger.exception(e)
        return (None, ResultStatus.MODULE_FAILURE)
    if extractor_status != ResultStatus.ALL_OKAY:
        return (None, extractor_status)
    logger.debug('Processed text: ' + extracted_text)

    try:
        entity_parser = text_service.DataParser()
        entities, parser_status = entity_parser.get_entities(extracted_text)
    except Exception as e:
        logger.exception(e)
        return (None, ResultStatus.MODULE_FAILURE)
    if parser_status != ResultStatus.ALL_OKAY:
        return (None, parser_status)
    logger.debug('Entities: ' + str(entities))
    return (entities, parser_status)
