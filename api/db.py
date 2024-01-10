from pymongo import MongoClient
from pymongo.errors import PyMongoError


class FileMetadataDB:
    def __init__(self, mongo_uri, db_name, logger):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection_name = "file_metadata"
        self.logger = logger

    def insert(self, metadata):
        result = self.db[self.collection_name].insert_one(metadata)
        return result

    def get(self, file_id: str):
        result = self.db[self.collection_name].find_one({"_id": file_id})
        return result

    def delete(self, file_id: str):
        result = self.db[self.collection_name].delete_one({"_id": file_id})
        return result

    def get_all(self):
        cursor = self.db[self.collection_name].find()
        return list(cursor)

    def get_paginated(self, page: int, limit: int, search_term: str = None):
        query = {}
        if search_term:
            # create case-insensitive regex pattern for searching file names
            query["file_name"] = {"$regex": search_term, "$options": "i"}

        # calculate skip based on page and limit
        skip = (page - 1) * limit
        cursor = self.db[self.collection_name].find(query).skip(skip).limit(limit)
        return list(cursor)

    def update(self, metadata):
        try:
            collection = self.db[self.collection_name]
            result = collection.update_one({"_id": metadata["_id"]}, {"$set": metadata})
            return result
        except PyMongoError as e:
            self.logger.error(f"Error updating file metadata: {str(e)}")
            raise
