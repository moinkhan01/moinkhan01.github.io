import pymongo
import certifi
from config import mongo_uri


mongo_uri = mongo_uri

try:
    client = pymongo.MongoClient(
        host= str(mongo_uri) , tlsCAFile=certifi.where())

    client.server_info()

    db = client["tvExchangeConnectorCurrency"]

except Exception as e:

    print("Error Occured while connecting to database",e)
