from datetime import timedelta
from durations_nlp import Duration

import nextcord
from nextcord.ext import commands

__all__ = (
    "Bot",
    "TimeDelta"
)

BOTS = {
    "deriver" : 704130818339242094,
    "pokecord": 705016654341472327,
    "pokemon" : 669228505128501258
}


class Bot(commands.Converter):
    async def convert(self, ctx, arg):
        arg = arg.strip()
        bot_name = arg.lower()

        if bot_name in ("deriver", "pokecord", "pokemon"):
            bot = ctx.bot.get_user(BOTS[bot_name])
            return bot

        raise commands.BadArgument(f"Could not find a bot matching `{arg}`.")


class TimeDelta(commands.Converter):
    async def convert(self, ctx, arg):
        try:
            duration = Duration(arg).to_seconds()
        except:
            raise commands.BadArgument(f"{arg} is not a valid duration.")

        if duration > 60 * 60 * 24 * 28:
            raise commands.BadArgument("Cannot mute for more than 28 days.")

        return nextcord.utils.utcnow() + timedelta(seconds=duration)