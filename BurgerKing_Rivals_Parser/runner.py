from scrapy.crawler import CrawlerProcess  # Импортируем класс для создания процесса
from scrapy.settings import Settings  # Импортируем класс для настроек

from BurgerKing_Rivals_Parser import settings  # Наши настройки
from BurgerKing_Rivals_Parser.spiders.burgerking import BurgerkingSpider  # Класс паука
from BurgerKing_Rivals_Parser.spiders.kfc import KfcSpider  # Класс второго паука

if __name__ == '__main__':
    crawler_settings = Settings()  # Создаем объект с настройками
    crawler_settings.setmodule(settings)  # Привязываем к нашим настройкам

    process = CrawlerProcess(settings=crawler_settings)  # Создаем объект процесса для работы
    process.crawl(BurgerkingSpider)
    process.crawl(KfcSpider)

    process.start()  # Пуск