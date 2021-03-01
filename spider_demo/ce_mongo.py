import pymongo


if __name__ == '__main__':
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    
    db = client['SC']
    info = db['acars'].find()
    print(len(list(info)))