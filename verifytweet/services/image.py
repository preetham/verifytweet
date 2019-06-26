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
import uuid
import subprocess

import pytesseract
import PIL

from werkzeug.utils import secure_filename

from verifytweet.shared.logging import logger
from verifytweet.config.settings import app_config


class Uploader(object):
    """Saves image file received from POST request.

    Saves image file to a temporary location received by
    Flask after checking valid file types.

    Attributes:
        file_obj: Image file, type: werkzeug.datastructures.FileStorage.
    """
    def __init__(self, file_obj):
        self.file = file_obj

    def save_to_disk(self):
        filename = secure_filename(self.file.filename)
        if self.file and self.allowed_file(filename):
            saved_file_name = str(uuid.uuid4()) + '.' + \
                filename.rsplit('.', 1)[1].lower()
            saved_file_path = os.path.join(app_config.FILE_DIRECTORY,
                                        saved_file_name)
            logger.info('Saving file to path: ' + saved_file_path)
            self.file.save(saved_file_path)
            return saved_file_path
        return None

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in app_config.ALLOWED_EXTENSIONS


class Extractor(object):
    """Extracts text from image

    Encapsulates image extraction process to text.

    Attributes:
        file_path: A string indicating file path where the image is stored.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def get_text(self):
        if not self.file_path:
            raise ValueError
        logger.info('Processing Image...')
        new_file_path = self.rescale(self.file_path)
        img = PIL.Image.open(new_file_path).convert('L')
        logger.info('Extracting text from rescaled image..')
        text = pytesseract.image_to_string(image=img)
        return text

    @staticmethod
    def rescale(file_path):
        if not file_path:
            raise ValueError
        logger.info('Rescaling Image to 300 dpi')
        new_file_path = file_path.rsplit('.', 1)[0] + '.jpg'
        cmd = [
            app_config.IMAGEMAGICK_PATH, file_path, '-bordercolor', 'White',
            '-resample', app_config.UPSCALE_RESOLUTION,
            '-border', '10x10', '-alpha', 'off', new_file_path
        ]
        subprocess.run(cmd)
        return new_file_path
