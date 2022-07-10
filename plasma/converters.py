from datetime import timedelta
from durations_nlp import Duration

import nextcord
from nextcord.ext import commands

from .mongo import mongo

__all__ = ("BotConverter", "SpeciesConverter", "TimeConverter", "RollConverter")


class BotConverter(commands.Converter):
    async def convert(self, ctx, arg):
        name = arg.lower()
        data = {
            "pokemon": 669228505128501258,
            "pokecord": 705016654341472327,
            "deriver": 704130818339242094
        }

        if name not in ("pokemon", "pokecord", "deriver"):
            raise commands.BadArgument(f"Could not find a bot matching `{arg}`.")

        bot = ctx.bot.get_user(data[name])
        return bot


class SpeciesConverter(commands.Converter):
    def __init__(self, *, show_error=True):
        self.show_error = show_error

    async def convert(self, ctx, arg):
        arg = arg.strip()
        if arg.isdigit():
            species = mongo.species_by_id(int(arg))
        else:
            species = mongo.species_by_name(arg.lower())

        if species is None:
            if self.show_error:
                raise commands.BadArgument(f"Could not find a pokemon matching `{arg}`.")
            else:
                return None
        return species


class TimeConverter(commands.Converter):
    async def convert(self, ctx, arg):
        try:
            duration = Duration(arg).to_days()
        except:
            raise commands.BadArgument(f"{arg} is not a valid duration.")

        if duration > 28:
            raise commands.BadArgument("Cannot mute for more than 28 days.")

        time = nextcord.utils.utcnow() + timedelta(days=duration)
        return time


class RollConverter(commands.Converter):
    async def convert(self, ctx, arg):
        arg = arg.strip()
        message = f"`{arg}` is not a valid range."

        if arg.isdigit():
            arg = int(arg)
            if arg <= 0:
                raise commands.BadArgument(message)
            return 1, arg

        if "-" in arg:
            try:
                loc   = arg.find("-")
                front = int(arg[:loc])
                rear  = int(arg[loc + 1:])
            except:
                raise commands.BadArgument(message)

            if front >= rear:
                raise commands.BadArgument(message)
            return front, rear

        raise commands.BadArgument(message)