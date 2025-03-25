import logging
import sys

logger = logging.getLogger('wtp-bot')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(message)s', '%d.%m.%Y %H:%M:%S')
handler.setFormatter(formatter)

logger.addHandler(handler)
