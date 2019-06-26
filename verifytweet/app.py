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


import os
import traceback

from flask import Flask, jsonify, request
from flask_cors import CORS

import verifytweet.services.image as image_service
import verifytweet.services.text as text_service
import verifytweet.services.search as search_service
import verifytweet.shared.date_checker as date_checker

from verifytweet.shared.logging import logger
from verifytweet.config.settings import app_config



router = Flask(__name__, static_folder = app_config.FILE_DIRECTORY)
router.config['MAX_CONTENT_LENGTH'] = app_config.MAX_CONTENT_LENGTH
cors = CORS(router, resources={r'/api/*': {'origins': '*'}})


@router.route('/health', methods=['GET'])
def health():
    logger.info('Health Check log')
    return jsonify({'status': 0})


@router.route('/api/v1/verify', methods=['POST'])
def verify_tweet():
    """Verifies tweet from given image.

    Verifies tweet from image received via POST request
    using a combination of image processing, text processing
    as well as a search service.

    Args:
        data: File object containing Image data.
        type: A string indicating the type of data: "image" or "link".

    Returns:
        A dict mapping status and validity of the tweet. For
        example:

        {
          "status": 0,
          "result": True
        }

        If the form fields are missing or the tweet is too old,
        a 400 (Bad Request) is returned.
    """
    logger.info('Received data for processing...')

    data_type = request.form['type']
    request_image = request.files['data']
    if not data_type or not request_image:
        return "Missing form fields", 400
    uploader = image_service.Uploader(request_image)
    file_path = uploader.save_to_disk()

    text_extractor = image_service.Extractor(file_path)
    extracted_text = text_extractor.get_text()
    logger.info('Processed text: ' + extracted_text)

    entity_parser = text_service.DataParser(extracted_text)
    entities = entity_parser.get_entities()
    logger.info('Entities: ' + str(entities))
    if not entities['date'] or not date_checker.valid_date(entities['date']):
        return "Date of Tweet too old", 400

    search_controller = search_service.SearchController(
        entities['user_id'], entities['date'])
    same_day_tweets = search_controller.aggregate_tweets()
    if not same_day_tweets:
        return jsonify({
            'status': 1,
            'result': False
        })

    text_processor = text_service.TextProcessor(entities['tweet'], same_day_tweets)
    similarity_matrix = text_processor.get_similarity()
    valid_tweet = verify_validity(similarity_matrix)
    logger.info('Tweet Validity: ' + str(valid_tweet))

    return jsonify({
        'status': 0,
        'result': valid_tweet
    })


def verify_validity(similarity_matrix):
    """Verifies validity of a tweet in similarity matrix.

    Verifies validity of a tweet in similarity matrix, if it crosses
    the configured threshold for similarity.

    Args:
        similarity_matrix: A list of lists containing similarity scores

    Returns:
        A Boolean representing validity of the tweet.
    """
    for row in similarity_matrix:
        for column in row:
            if column > app_config.SIMILARITY_THRESHOLD:
                return True
    return False