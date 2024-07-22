from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from foodbazaar.items import FoodbazaarItem

from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By  # noqa

import time


class FoodSpider(CrawlSpider):
    name = "food"
    allowed_domains = ["shop.foodbazaar.com"]
    start_urls = ["https://shop.foodbazaar.com/store/food-bazaar/storefront"]
    link_extractor = LinkExtractor(
        restrict_xpaths='//nav[@id="sm-departments"]',
        process_value=lambda x: f'https://shop.foodbazaar.com{x}'
    )

    def start_requests(self) -> Iterable[Request]:
        yield SeleniumRequest(
            url=self.start_urls[0],
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        driver = response.meta['driver']
        driver.get('https://shop.foodbazaar.com/store/food-bazaar/storefront')

        btn_cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        btn_cookies.click()
        time.sleep(2)
        btn_zip = driver.find_element(By.CLASS_NAME, 'e-okf0s9')
        btn_zip.click()
        time.sleep(2)

        a_elements = driver.find_elements(
            By.XPATH,
            '//nav[@aria-labelledby="sm-departments"]//a'
        )
        departments = [x.get_attribute('href') for x in a_elements]

        for dp in departments:
            driver.get(dp)
            category_elements = driver.find_elements(
                By.XPATH,
                '//ul[@class="e-1jkorx6"]//a[@class="e-18z2zel"]'
            )
            links = [x.get_attribute('href') for x in category_elements]

            for link in links:
                driver.get(link)
                time.sleep(2)

                i = 1
                num_scrolls = 2
                last_height = driver.execute_script("return document.body.scrollHeight")

                while True and i <= num_scrolls:
                    i += 1
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                r = Selector(text=driver.page_source)

                containers = r.xpath('//div[@class="e-13udsys"]')

                for container in containers[1:]:
                    item = ItemLoader(
                        item=FoodbazaarItem(),
                        response=r,
                        selector=container
                    )

                    item.add_xpath('name', './/h2/text()')
                    item.add_xpath(
                        'price',
                        './/div[@class="e-1s49gp4" or @class="e-1jioxed"]/span[1]/text()'
                    )
                    item.add_xpath(
                        'link',
                        './/a[@class="e-1dlf43s"]/@href'
                    )

                    yield item.load_item()
