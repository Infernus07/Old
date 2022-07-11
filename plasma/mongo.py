from pymongo import MongoClient

from .utils import title

__all__ = ("Mongo", "mongo")


class Mongo:
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://Infernus:PgtrAv4wGteOfe2s@plasma.f6kiu.mongodb.net/test")
        self.db = self.cluster["plasma"]

        # Collections

        self.member = self.db["member"]
        self.pokemon = self.db["pokemon"]
        self.tag = self.db["tag"]

    def species_by_name(self, name):
        name = title(name.strip())
        doc = self.pokemon.find_one({"alias": name})
        if doc is None:
            return None
        return doc

    def species_by_id(self, id):
        doc = self.pokemon.find_one({"_id": id})
        if doc is None:
            return None
        return doc

    def register(self, member):
        doc = {
            "_id": member.id,
            "name": member.name,
            "reps": 0,
            "warns": 0,
            "pokemon": [],
            "pokecord": [],
            "deriver": []
        }
        return self.member.insert_one(doc)

    def find_member(self, member):
        doc = self.member.find_one({"_id": member.id})
        if doc is None:
            self.register(member)

        doc = self.member.find_one({"_id": member.id})
        return doc

    def update_member(self, member, update):
        doc = self.member.find_one({"_id": member.id})
        if doc is None:
            self.register(member)
            
        return self.member.update_one({"_id": member.id}, update)


mongo = Mongo()