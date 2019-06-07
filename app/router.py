import os
import traceback

from flask import Flask, jsonify, request

from app.logger import logger
from app.config.config import app_config

app_router = Flask(__name__)


@app_router.route('/health', methods=['GET'])
def health():
    logger.info('Health Check log')
    return jsonify({'status': 0})


@app_router.route('/process', methods=['POST'])
def process():
    social_network = request.form['social']
    data_type = request.form['type']
    request_image = request.files['data']
