import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S', handlers=[
        logging.FileHandler("depop_scraper.log")])

logger = logging.getLogger(__name__)

