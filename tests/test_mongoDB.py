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

mongo = MongoDB(db_name)
def test_insert_element():
    mongo.insert_document("users", data)
def test_count_documents():
    result = mongo.count_documents()
    print(result)
def test_get_all_documents():
    results = mongo.find_documents('posts', {})
    for i in results:
        print(i)
def test_update_element():
    mongo.update_document('users', {"_id": ObjectId('66de10020b7fd6d2e67fe144')}, {"age": 31})

def test_delete_all():
    db_name = "posts"
    results = mongo.find_documents(db_name, {})
    for element in results:
        id = element["_id"]
        mongo.delete_documents(db_name, {'_id': id })