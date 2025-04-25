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


class Info_Parser:

    def __init__(self):
        self.browser = None
        self.page = None
        self.context = None
        self.item_info = []
        self.playwright = None

    def launch_browser(self):

        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()

        self.page = self.context.new_page()

    def close_browser(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()
        logger.info("Browser closed")

    def get_info(self, url, desired_price: float):
        logger.info(f"{url} to parse")
        self.page.goto(url)
        try:
            title = self.page.wait_for_selector("h1.styles_title__kWcg1", timeout=5000)  # title
            price_selector = self.page.wait_for_selector('p.styles_price__H8qdh', timeout=5000)  # price

            if not title:
                logger.info(f"No title for this item")
                price = float(price_selector.text_content().replace("$", "").strip().replace(",", ""))
                if desired_price <= price:
                    logger.info(f"Regular price: {price}")
                    self.item_info.append({"url": url, "price": price})
            else:
                price = float(price_selector.text_content().replace("$", "").strip().replace(",", ""))
                if desired_price <= price:
                    logger.info(f"Url: {url}, Title: {title,} regular price: {price}")
                    self.item_info.append({"Url": url, "title": title, "price": price})
        except Exception as e:
            logger.error(f"Error parsing item info: {e}")

    def accept_cookies(self):
        try:
            self.page.get_by_role("button", name="Accept").click()
        except Exception as e:

            logger.info("Cookies button not found")

    def run(self, desired_price):
        while True:
            response = requests.get(f"{HOST}/get")
            if response.status_code == 404:
                time.sleep(5)
            else:
                self.get_info(response.text, desired_price)

    def launcher(self, desired_price):
        self.launch_browser()
        # self.accept_cookies()
        self.run(desired_price)
        self.close_browser()


app = Info_Parser()
app.launcher(30)