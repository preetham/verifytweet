from pytesseract import image_to_string
from PIL import Image, ImageFilter, ImageEnhance

from app.logger.logger import logger

def get_text(file_path):
    if not file_path:
        raise ValueError
    logger.info('Processing Image...')
    img = Image.open(file_path).convert('L')
    img = img.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)
    img = img.convert('1')
    text = image_to_string(img)
    return text
