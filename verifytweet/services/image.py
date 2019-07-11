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
import subprocess
import uuid

import PIL
import pytesseract

from verifytweet.util.logging import logger
from verifytweet.config.settings import app_config
from verifytweet.util.result import ResultStatus


class Extractor(object):
    """Extracts text from image

    Encapsulates image extraction process to text.

    Attributes:
        file_path: A string indicating file path where the image is stored.
    """

    def __init__(self):
        pass

    def get_text(self, file_path: str):
        """Extracts text from image
        """
        if not isinstance(file_path, str):
            raise TypeError('File path must be type string')
        if not file_path:
            raise ValueError('File path cannot be empty')
        logger.info('Processing Image...')
        try:
            new_file_path = self.rescale(file_path)
            logger.info('Extracting text from rescaled image...')
            img = PIL.Image.open(new_file_path)
            text = pytesseract.image_to_string(image=img)
            try:
                os.remove(new_file_path)
            except Exception as e:
                logger.exception(e)
            if not text:
                return (None, ResultStatus.NO_RESULT)
            return (text, ResultStatus.ALL_OKAY)
        except Exception as e:
            logger.exception(e)
            return (None, ResultStatus.MODULE_FAILURE)

    @staticmethod
    def rescale(file_path):
        if not isinstance(file_path, str):
            raise TypeError('File path must be type string')
        if not file_path:
            raise ValueError('File path cannot be empty')
        logger.info('Rescaling Image to 300 dpi...')
        new_file_path = os.path.join(app_config.FILE_DIRECTORY,
                                     str(uuid.uuid1()) + '.png')
        cmd = [
            'convert', file_path, '-resample', '300x300',
            '-alpha', 'off', '-colorspace', 'Gray', '-threshold', '75%',
            '-density', '300x300', '-units', 'PixelsPerCentimeter', '-blur',
            '1x65000', '-level', '50x100%', new_file_path
        ]
        completed_process = subprocess.run(cmd)
        completed_process.check_returncode()
        return new_file_path
