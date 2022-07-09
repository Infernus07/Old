import plasma
from pymongo import MongoClient

from nextcord.ext import commands


class Mongo(commands.Cog):
    """For database operations."""

    def __init__(self, bot):
        self.bot = bot
        self.db = MongoClient(plasma.DATABASE_URI)["plasma"]

def setup(bot):
    bot.add_cog(Mongo(bot))