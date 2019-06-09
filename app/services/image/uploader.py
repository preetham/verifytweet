import os
import uuid

from concurrent.futures import ThreadPoolExecutor
from werkzeug.utils import secure_filename

from app.logger.logger import logger
from app.config.config import app_config


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app_config.ALLOWED_EXTENSIONS


def save_to_disk(file_obj):
    filename = secure_filename(file_obj.filename)
    if file_obj and allowed_file(filename):
        saved_file_name = str(uuid.uuid4()) + '.' + \
            filename.rsplit('.', 1)[1].lower()
        saved_file_path = os.path.join(
            app_config.FILE_DIRECTORY, saved_file_name)
        logger.info('Saving file to path: ' + saved_file_path)
        file_obj.save(saved_file_path)
        return saved_file_path
    return None
