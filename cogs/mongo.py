from pymongo import MongoClient

from nextcord.ext import commands


class Mongo(commands.Cog):
    """For database operations."""

    def __init__(self, bot):
        self.bot = bot
        self.db = MongoClient("mongodb+srv://Infernus:PgtrAv4wGteOfe2s@plasma.f6kiu.mongodb.net/test")["plasma"]

def setup(bot):
    bot.add_cog(Mongo(bot))