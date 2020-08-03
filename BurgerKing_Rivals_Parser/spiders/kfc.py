import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from BurgerKing_Rivals_Parser.items import BurgerkingRivalsParserItem
from geopy.geocoders import Nominatim, ArcGIS
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class KfcSpider(scrapy.Spider):
    name = 'kfc'
    allowed_domains = ['kfc.ru']
    start_urls = ['https://www.kfc.ru/restaurants']

    def __init__(self):
        self.city = 'Москва'
        self.fox_options = Options()
        self.fox_options.add_argument('-headless')
        self.driver = webdriver.Firefox(options=self.fox_options)
        super().__init__()

    def parse(self, response):
        self.driver.get(response.url)
        # Ищем и нажимаем на кнопку со списком ресторанов
        rest_list_button = self.driver.find_element_by_xpath('/html[1]/body[1]/div[1]/div[1]/div[2]/'
                                                      'div[1]/div[2]/div[2]/button[2]')
        rest_list_button.click()
        # Собираем список всех ресторанов
        rest_list = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'Mujm2VkJ7g'))
        )
        for rest in rest_list:  # Парсим полученные рестораны на предмет адреса
            address = rest.find_element_by_class_name('_2XllDYbBnt').text
            if self.city in address:
                # В случае если ресторан находится в искомом городе получаем его координаты
                geolocator = ArcGIS(
                    user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0")
                location_geo = geolocator.geocode(address)
                yield BurgerkingRivalsParserItem(latitude=location_geo.latitude,
                                                 longitude=location_geo.longitude,
                                                 city=self.city,
                                                 address=address,
                                                 brand='kfc')

    def __del__(self):
        self.driver.quit()
        print('Selenium closed')
