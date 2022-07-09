from plasma import DATABASE_URI
from pymongo import MongoClient

from nextcord.ext import commands


class Mongo(commands.Cog):
    """For database operations."""

    def __init__(self, bot):
        self.bot = bot
        self.db = MongoClient(DATABASE_URI)["plasma"]

def setup(bot):
    bot.add_cog(Mongo(bot))