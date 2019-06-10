import subprocess

from pytesseract import image_to_string
from PIL import Image, ImageFilter, ImageEnhance

from app.logger.logger import logger
from app.config.config import app_config



def get_text(file_path):
    if not file_path:
        raise ValueError
    logger.info('Processing Image...')
    new_file_path = rescale(file_path)
    img = Image.open(new_file_path).convert('L')
    logger.info('Extracting text from rescaled image..')
    text = image_to_string(img)
    return text

def rescale(file_path):
    if not file_path:
        raise ValueError
    logger.info('Rescaling Image to 300 dpi')
    new_file_path = file_path.rsplit('.', 1)[0] + '.jpg'
    cmd = app_config.IMAGEMAGICK_PATH + ' -resize ' + \
        app_config.UPSCALE_PERCENTAGE + ' ' + file_path + \
        ' ' + new_file_path
    subprocess.call(cmd, shell=True)
    return new_file_path
