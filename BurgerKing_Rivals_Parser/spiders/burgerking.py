import scrapy
from scrapy.http import HtmlResponse
from BurgerKing_Rivals_Parser.items import BurgerkingRivalsParserItem


class BurgerkingSpider(scrapy.Spider):
    name = 'burgerking'
    allowed_domains = ['burgerking.ru']
    # Получаем список всех заведений в России
    start_urls = ['https://burgerking.ru/restaurant-locations-json-reply-new/']

    def __init__(self):
        self.city = 'Москва'
        super().__init__()

    def parse(self, response):
        # Получаем координаты заведения, его Id и формируем ссылку для перехода
        all_burger_restaurants = response.json()
        for i in range(len(all_burger_restaurants)):
            storeid = all_burger_restaurants[i]["storeId"]
            latitude = all_burger_restaurants[i]["latitude"]
            longitude = all_burger_restaurants[i]["longitude"]
            restaurant_link = f'https://burgerking.ru/map-markers-info?' \
                              f'storeId={storeid}&lat=&lon='
            yield response.follow(restaurant_link, callback=self.restaurant_parse,
                                  meta={'latitude': latitude, 'longitude': longitude})

    def restaurant_parse(self, response: HtmlResponse):
        # Получаем город и адрес заведения
        restaurant_city = response.css('p.over-bubble-city::text').extract_first()
        restaurant_address = response.css('p.address1::text').extract_first()
        if self.city == restaurant_city:
            yield BurgerkingRivalsParserItem(latitude=response.meta['latitude'],
                                             longitude=response.meta['longitude'],
                                             city=restaurant_city,
                                             address=restaurant_address,
                                             brand='burgerking')
