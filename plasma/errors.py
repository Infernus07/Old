__all__ = (
    "DiscordException",
    "PokemonNotFound"
)

class DiscordException(Exception):
    def __init__(self, message = None, *args):
        if message is not None:
            m = message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
            super().__init__(m, *args)
        else:
            super().__init__(*args)


class NotInGuild(DiscordException):
    pass


class PokemonNotFound(DiscordException):
    def __init__(self, pokemon_name):
        super().__init__(f"Could not find a pokemon matching `{pokemon_name}`.")