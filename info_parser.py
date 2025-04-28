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

def get_info(url, desired_price: float):
    logger.info(f"{url} to parse")
    page.goto(url)
    try:
        title = page.wait_for_selector("h1.styles_title__kWcg1", timeout=5000)  # title
        price_selector = page.wait_for_selector('p.styles_price__H8qdh', timeout=5000)  # price
        price = float(price_selector.text_content().replace("$", "").strip().replace(",", ""))
        if not title:

            item_info = {"price": price, "url": url}
            if price <= desired_price:
                print(f"No title for this item; {item_info}")
        else:
            title = title.text_content().strip()
            item_info = {"title": title, "price": price, "url": url}
            if price <= desired_price:
                print(item_info)
    except Exception as e:
        print("Error")

def run(desired_price: float):
    while True:
        response = requests.get(f"{HOST}/get")
        if response.status_code == 404:
            time.sleep(5)
        else:
            data = response.json()
            attribute = data.get("url")

            get_info(attribute, desired_price)

run(25.00)


