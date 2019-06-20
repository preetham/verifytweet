import logging as logger
import sys

root = logger.getLogger()
root.setLevel(logger.DEBUG)
handler = logger.StreamHandler(sys.stdout)
handler.setLevel(logger.DEBUG)
formatter = logger.Formatter(u'%(asctime)s -- %(levelname)s -- %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)
