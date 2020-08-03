from pymongo import MongoClient


class BurgerkingRivalsParserPipeline:

    def process_item(self, item, spider):
        return item


class DataBasePipeline:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.burgerking_rivals

    def process_item(self, item, spider):
        self.coord_converter(item)
        collection = self.mongo_base['burgerking_rivals']
        location = {'type': 'Point', 'coordinates': [item['longitude'], item['latitude']]}
        # Если адреса нет в БД, то добавляем запись
        collection.update_one({'address': item['address']},
                              {"$set": {'address': item['address'], 'city': item['city'],
                                        'location': location, 'brand': item['brand']}}, upsert=True)
        return item

    def __del__(self):
        self.client.close()

    def coord_converter(self, item):
        if not isinstance(item['longitude'], float):
            item['longitude'] = float(item['longitude'])
            item['latitude'] = float(item['latitude'])
