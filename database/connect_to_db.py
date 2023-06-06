from pymongo import MongoClient

# Establishing the connection with the database
def connect_to_mongodb():
    client = MongoClient("mongodb+srv://amnewsing:hmIiNbPsAeOgohyA@fypcluster.yuntl03.mongodb.net/?retryWrites=true&w=majority")
    db = client["test"]
    return client, db