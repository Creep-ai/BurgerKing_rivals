from pymongo import MongoClient


def count_rivals():
    client = MongoClient('localhost', 27017)
    db = client['burgerking_rivals']
    bk = db.burgerking_rivals
    # bk.create_index([('location', pymongo.GEOSPHERE)], name='2km_near')
    # print(bk.index_information())
    # Считаем кол-во ресторанов KFC в радиусе 2 км от каждого ресторана BurgerKing:
    for burger_rest in bk.find({'brand': 'burgerking'}):
        query = {'$and':
            [
                {'location':
                     {'$geoWithin':
                          {'$centerSphere': [burger_rest['location']['coordinates'], 2 / 6378.1]}
                      }
                 },
                {'brand': 'kfc'}
            ]
        }
        n_rivals = bk.count_documents(query)
        bk.update_one(burger_rest, {'$set': {'n_rivals': n_rivals}}, upsert=True)
    client.close()
