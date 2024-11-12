from tests.mongo_db import MongoDB
from bson import ObjectId
db_name = "db_test"
db_collection = "collection_test"

# Create a new client and connect to the server
data = {
    "name": "John Doe",
    "age": 30,
    "job": "Software Developer"
}

mongo = MongoDB(db_name, db_collection)
def test_insert_element():
    mongo.insert_document(data)
def test_count_documents():
    result = mongo.count_documents()
    print(result)
def test_get_all_documents():
    results = mongo.find_documents({})
    for i in results:
        print(i)
def test_update_element():
    mongo.update_document({"_id": ObjectId('66de10020b7fd6d2e67fe144')}, {"age": 31})
