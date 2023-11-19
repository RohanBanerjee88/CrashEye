from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from detect import detect_error_type

uri = "mongodb+srv://AdityaAA2004:crasheye%40526%23MSU@atlascluster.okb9ixx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api = ServerApi('1'))
# Send a ping to confirm a successful connection

def upload_crash_to_mongo(data):
    try:
        db = client["CrashLogs"]
        collection = db[data[9].capitalize()]
        json_data = {}
        json_data["fname"]= data[0]
        json_data["tstamp"]= data[1]
        json_data["System"]=data[2]
        json_data["Node"] = data[3]
        json_data["Release Date"] = data[4]
        json_data["Version"]= data[5]
        json_data["Machine"]= data[6]
        json_data["Processor"]= data[7]
        json_data["RAM Usage"]= data[8]
        json_data["Class"]= data[9]
        json_data["GPU"]= data[10]
        res = collection.insert_one(json_data)
        print("Stored")
    except Exception as e:
        print("An error: ", str(e))





