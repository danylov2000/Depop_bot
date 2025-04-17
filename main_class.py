from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError

import functions
from logger import *
import time


class App:

    def __init__(self, email):
        self.email = email
        self.browser = None
        self.page = None
        self.collected_urls = set()

    def launch_browser(self):
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        logger.info("Browser launched")

    def close_browser(self):
        self.browser.close()
        logger.info("Browser closed")

    def goto_homepage(self):
        self.page.goto("https://www.depop.com/")

        logger.info("Navigated to Depop")

    def accept_cookies(self):
        try:
            self.page.get_by_role("button", name="Accept").click()
        except Exception as e:

            logger.info("Cookies button not found")

    def search(self, text):

        self.page.locator("#searchBar__input").first.fill(text)
        self.page.keyboard.press("Enter")


        items = self.page.locator("li.styles_listItem__Uv9lb").all()
        return items

    def collect_urls(self):
        current_element = 0
        total_items = self.page.locator("#main > div > div.styles_header__lny1Z > div > h1 > span._text_bevez_41._shared_bevez_6._normal_bevez_51.styles_searchQuerySecondary__j_1rr").first.text_content()
        total_items = int(total_items.strip("(").strip(" results)"))
        urls = self.page.locator('ol.styles_productGrid__Cpzyf a.styles_unstyledLink__DsttP')
        try:
            while current_element <= total_items:
                if self.page.locator("styles_loaderWrapper__RDUnD").first.is_visible():
                    time.sleep(1)
                    continue

                url = urls.nth(current_element)
                url.scroll_into_view_if_needed()
                self.page.mouse.wheel(0, 50)

                attribute = url.get_attribute("href")
                self.collected_urls.add(attribute)
                url.highlight()

                current_element += 1
        except TimeoutError:
            logger.info("Parsing finished")


    # styles_loaderWrapper__RDUnD

    def run(self, search_text):
        self.launch_browser()
        self.goto_homepage()
        self.accept_cookies()
        self.search(search_text)
        self.collect_urls()
        # self.scrape_items()
        self.close_browser()
