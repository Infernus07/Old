from pymongo import MongoClient

__all__ = (
    "Mongo",
    "mongo"
)


class Mongo:
    @property
    def db(self):
        return MongoClient("mongodb+srv://Infernus:PgtrAv4wGteOfe2s@plasma.f6kiu.mongodb.net/test")["plasma"]


mongo = Mongo