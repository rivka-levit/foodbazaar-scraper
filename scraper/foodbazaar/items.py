import scrapy
from itemloaders.processors import Join  # noqa


def clean_price(item):
    return item[0].replace('Current price: ', '')


def clean_link(item):
    return f'https://shop.foodbazaar.com{item[0]}'


class FoodbazaarItem(scrapy.Item):  # noqa
    name = scrapy.Field(output_processor=Join())
    price = scrapy.Field(output_processor=clean_price)
    link = scrapy.Field(output_processor=clean_link)
