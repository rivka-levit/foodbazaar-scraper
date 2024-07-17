import scrapy


class FoodSpider(scrapy.Spider):
    name = "food"
    allowed_domains = ["shop.foodbazaar.com"]
    start_urls = ["https://shop.foodbazaar.com/store/food-bazaar/storefront"]

    def parse(self, response, **kwargs):
        pass
