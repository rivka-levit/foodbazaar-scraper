from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

from foodbazaar.items import FoodbazaarItem

from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By

import time


class FoodSpider(scrapy.Spider):
    name = "food"
    allowed_domains = ["shop.foodbazaar.com"]
    start_urls = ["https://shop.foodbazaar.com/store/food-bazaar/collections/n-fresh-fruits-51483"]

    def start_requests(self) -> Iterable[Request]:
        yield SeleniumRequest(
            url=self.start_urls[0],
            wait_time=5,
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        driver = response.meta['driver']
        btn_cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        btn_cookies.click()
        time.sleep(2)
        btn_zip = driver.find_element(By.CLASS_NAME, 'e-okf0s9')
        btn_zip.click()
        time.sleep(2)

        r = Selector(text=driver.page_source)

        containers = r.xpath('//div[@class="e-13udsys"]')

        for container in containers:
            item = ItemLoader(
                item=FoodbazaarItem(),
                response=r,
                selector=container
            )

            item.add_xpath('name', './/h2/text()')
            item.add_xpath(
                'price',
                './/div[@class="e-1s49gp4"]/span[1]/text()'
            )
            item.add_xpath(
                'link',
                './/a[@class="e-1dlf43s"]/@href'
            )

            yield item.load_item()
