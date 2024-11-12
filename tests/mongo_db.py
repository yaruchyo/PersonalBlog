from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()


MONGO_DB_PASS = os.getenv("MONGO_DB_PASS")
MONGO_DB_USER = os.getenv("MONGO_DB_USER")


class MongoDB:

    def __init__(self, db_name: str, collection_name: str):
        """
        Initializes the MongoDB helper class.
        :param db_name: Database name.
        :param collection_name: Collection name.
        """
        uri = f"mongodb+srv://{MONGO_DB_USER}:{MONGO_DB_PASS}@cluster0.5f8va.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(uri, server_api=ServerApi('1'))

        # Check connection
        try:
            self.client.admin.command('ping')
            print("Connected to MongoDB")
        except ConnectionFailure as e:
            print("Could not connect to MongoDB", e)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_document(self, document: dict):
        """
        Inserts a single document into the collection.
        :param document: Dictionary representing the document.
        :return: Inserted ID.
        """
        result = self.collection.insert_one(document)
        return result.inserted_id

    def insert_many_documents(self, documents: list):
        """
        Inserts multiple documents into the collection.
        :param documents: List of dictionaries representing documents.
        :return: List of inserted IDs.
        """
        result = self.collection.insert_many(documents)
        return result.inserted_ids

    def find_document(self, query: dict):
        """
        Finds a single document matching the query.
        :param query: Dictionary representing the query.
        :return: Matching document or None if not found.
        """
        return self.collection.find_one(query)

    def find_documents(self, query: dict, limit: int = 0):
        """
        Finds multiple documents matching the query.
        :param query: Dictionary representing the query.
        :param limit: Limit the number of documents returned (default is 0, meaning no limit).
        :return: List of matching documents.
        """
        return list(self.collection.find(query).limit(limit))

    def update_document(self, query: dict, update_data: dict):
        """
        Updates a single document that matches the query.
        :param query: Dictionary representing the query.
        :param update_data: Dictionary representing the fields to update.
        :return: The updated document.
        """
        result = self.collection.update_one(query, {'$set': update_data})
        return result.modified_count

    def delete_document(self, query: dict):
        """
        Deletes a single document matching the query.
        :param query: Dictionary representing the query.
        :return: Number of documents deleted.
        """
        result = self.collection.delete_one(query)
        return result.deleted_count

    def delete_documents(self, query: dict):
        """
        Deletes multiple documents matching the query.
        :param query: Dictionary representing the query.
        :return: Number of documents deleted.
        """
        result = self.collection.delete_many(query)
        return result.deleted_count

    def count_documents(self, query: dict = {}):
        """
        Counts the number of documents in the collection that match the query.
        :param query: Dictionary representing the query.
        :return: Number of matching documents.
        """
        return self.collection.count_documents(query)

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        self.client.close()
