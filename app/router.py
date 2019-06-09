import os
import traceback

from flask import Flask, jsonify, request

from app.logger.logger import logger
from app.services.image import uploader, processor
from app.services.nlp.processor import get_entities
from app.config.config import app_config

app_router = Flask(__name__, static_folder=app_config.FILE_DIRECTORY)


@app_router.route('/health', methods=['GET'])
def health():
    logger.info('Health Check log')
    return jsonify({'status': 0})


@app_router.route('/api/v1/verify', methods=['POST'])
def get_text_from_image():
    logger.info('Received data for processing...')
    social_network = request.form['social']
    data_type = request.form['type']
    request_image = request.files['data']
    if not social_network or not data_type or not request_image:
        return "Missing valid data", 400
    file_path = uploader.save_to_disk(request_image)
    text = processor.get_text(file_path)
    logger.info('Processed text: ' + text)
    entities = get_entities(text)
    logger.info('Entities: ' + str(entities))
    return jsonify({
        'status': 0,
        'result': entities
    })
