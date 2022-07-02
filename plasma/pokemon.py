from .embed import Embed
from .mongo import Mongo

__all__ = (
    "Pokemon",
    "pokemon"
)


class Pokemon:
    def __init__(self, pokemon: str):
        self._pokemon = Mongo.search_pokemon(pokemon)

    @property
    def id(self) -> int:
        return self._pokemon["_id"]

    @property
    def name(self) -> str:
        return self._pokemon["name"]

    @property
    def description(self) -> str:
        return self._pokemon["description"]

    @property
    def evolution(self) -> str:
        return self._pokemon["evolution"]

    @property
    def hash(self) -> str:
        return self._pokemon["hash"]

    @property
    def region(self) -> str:
        return self._pokemon["region"]

    @property
    def height(self) -> str:
        return str(self._pokemon["height"]) + " m"

    @property
    def weight(self) -> str:
        return str(self._pokemon["weight"]) + " kg"

    @property
    def family(self) -> list:
        _family = []
        for i in self._pokemon["family"]:
            _family.append(Pokemon(i))

        return _family

    @property
    def hashes(self) -> list:
        return self._pokemon["hashes"]

    @property
    def names(self) -> list:
        return self._pokemon["names"]

    @property
    def rarity(self) -> list:
        return self._pokemon["rarity"]

    @property
    def types(self) -> list:
        return self._pokemon["types"]

    @property
    def base_stats(self) -> dict:
        return self._pokemon["base_stats"]

    @property
    def weak_embed(self) -> Embed:
        embed = self._pokemon["weak"]
        embed.update({"type": "rich"})
        return Embed.from_dict(embed)


pokemon = Pokemon