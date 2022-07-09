from nextcord.ext import commands

__all__ = (
    "Bot",
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