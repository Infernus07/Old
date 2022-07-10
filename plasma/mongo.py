from pymongo import MongoClient

from nextcord.ext import commands

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

    def insert_tag(self, *, name, content, owner_id):
        name = name.strip()
        content = content.strip()
        doc = {
            "_id": name.lower(),
            "alias": [],
            "content": content,
            "owner_id": owner_id,
            "uses": 0
        }
        tag = self.find_tag(name, raise_error=False)
        if tag is not None:
            raise commands.BadArgument(f"A tag with the name `{name}` already exists.")
        
        return self.tag.insert_one(doc)

    def find_tag(self, name, *, raise_error=True):
        name = name.strip()
        doc = self.tag.find_one({"alias": name.lower()})
        if doc is None and raise_error:
            raise commands.BadArgument(f"Could not find a tag matching `{name}`.")
        return doc

    def update_tag(self, name, update):
        doc = self.find_tag(name)
        return self.tag.update_one({"_id": doc["_id"]}, update)


mongo = Mongo()