import pymongo


__all__ = ["mongo_manager"]


class MongoManager:

    def __init__(self, uri='mongodb://localhost:27017/', db='doc_mainnet_rewards'):

        self.uri = uri
        self.db = db

    def set_connection(self, uri='mongodb://localhost:27017/', db='doc_mainnet_rewards'):

        self.uri = uri
        self.db = db

    def connect(self):

        uri = self.uri
        client = pymongo.MongoClient(uri)

        return client

    def collection_mocin_rewards(self, client, start_index=True):

        mongo_db = self.db
        db = client[mongo_db]
        collection = db['mocin_rewards']

        # index creation
        #if start_index:
        #    collection.create_index([('block_number', pymongo.DESCENDING)], unique=True)

        return collection

    def collection_mocin_rewards_extscaninfo(self, client, start_index=True):

        mongo_db = self.db
        db = client[mongo_db]
        collection = db['mocin_rewards_extscaninfo']

        # index creation
        #if start_index:
        #    collection.create_index([('block_number', pymongo.DESCENDING)], unique=True)

        return collection

    def collection_mocin_agent_tx(self, client, start_index=True):

        mongo_db = self.db
        db = client[mongo_db]
        collection = db['mocin_agent_tx']

        # index creation
        #if start_index:
        #    collection.create_index([('block_number', pymongo.DESCENDING)], unique=True)

        return collection


mongo_manager = MongoManager()
