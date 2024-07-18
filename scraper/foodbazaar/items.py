import scrapy
from itemloaders.processors import Join  # noqa


class FoodbazaarItem(scrapy.Item):  # noqa
    name = scrapy.Field(output_processor=Join())
    price = scrapy.Field(output_processor=Join())
    link = scrapy.Field(output_processor=Join())
