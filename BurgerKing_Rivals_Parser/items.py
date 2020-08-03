import scrapy


class BurgerkingRivalsParserItem(scrapy.Item):
    _id = scrapy.Field()
    brand = scrapy.Field()
    # storeId = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    address = scrapy.Field()
    city = scrapy.Field()
