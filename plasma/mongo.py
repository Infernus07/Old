from pymongo import MongoClient

from .errors import PokemonNotFound

__all__ = (
    "Mongo",
    "mongo"
)


class Mongo:
    db = MongoClient("mongodb+srv://Infernus:PgtrAv4wGteOfe2s@plasma.f6kiu.mongodb.net/test")["plasma"]

    @classmethod
    def search_pokemon(self, name: str, *, raise_error: bool = True) -> dict | None:
        pokemon = self.db["pokemon"].find_one({"names": name.strip().capitalize()})
        if pokemon is None:
            if raise_error:
                raise PokemonNotFound(name)
            return None

        return pokemon


mongo = Mongo