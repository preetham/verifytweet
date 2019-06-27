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

from flask import Flask, jsonify, request
from flask_cors import CORS

import verifytweet.services.controller as controller
import verifytweet.services.image as image_service

from verifytweet.util.logging import logger
from verifytweet.config.settings import app_config
from verifytweet.util.result import ResultStatus

router = Flask(__name__, static_folder=app_config.FILE_DIRECTORY)
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
    try:
        uploader = image_service.Uploader(request_image)
        file_path = uploader.save_to_disk()
        rest_controller = controller.NonAPIApproach(file_path)
    except Exception as e:
        logger.exception(e)
        return jsonify({
            'status': ResultStatus.MODULE_FAILURE.value,
            'result': None
        })
    tweet_validity, controller_status = rest_controller.exec()
    return jsonify({
        'status': controller_status.value,
        'result': tweet_validity
    })
