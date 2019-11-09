import pymongo
import pandas as pd


client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client['SC']['acars']

data = db.find()

# print(data)

df = pd.DataFrame(data=data)
# print(df)
print(df.info())