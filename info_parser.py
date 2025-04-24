from playwright.sync_api import sync_playwright
import requests
import time
import logging
HOST = "http://127.0.0.1:5000"

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)


playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
context = browser.new_context()

page = context.new_page()

def get_info(url):
    logger.info(f"{url} to parse")
    page.goto(url)
    title = page.wait_for_selector("h1.styles_title__kWcg1", timeout=5000)  # title
    price_selector = page.wait_for_selector('p.styles_price__H8qdh', timeout=5000)  # price
    price = float(price_selector.text_content().replace("$", "").strip().replace(",", ""))
    title = title.text_content().strip()
    print(price, title)

def run():
    while True:
        response = requests.get(f"{HOST}/get")
        if response.status_code == 404:
            time.sleep(5)
        else:
            get_info(response.text)

run()


