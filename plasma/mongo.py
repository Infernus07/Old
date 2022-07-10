from pymongo import MongoClient

__all__ = ("Mongo", "mongo")


class Mongo:
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://Infernus:PgtrAv4wGteOfe2s@plasma.f6kiu.mongodb.net/test")
        self.db = self.cluster["plasma"]

        # Collections

        self.pokemon = self.db["pokemon"]

    def species_by_name(self, name):
        doc = self.pokemon.find_one({"names": name})
        if doc is None:
            return None
        return doc

    def species_by_id(self, id):
        doc = self.pokemon.find_one({"_id": id})
        if doc is None:
            return None
        return doc


mongo = Mongo()