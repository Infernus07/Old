from PIL import Image
import aiohttp
from contextlib import suppress
from datetime import datetime
import hashlib
import io
import plasma

import nextcord
from nextcord.ext import commands


class Pokemon(commands.Cog):
    """For pokemon."""

    def __init__(self, bot):
        self.bot = bot
        self.col = plasma.mongo.pokemon
        self.session = aiohttp.ClientSession()

    def get_hash(self, bot):
        m = hashlib.md5()
        with open(f"assets/{bot}.png", "rb") as f:
            while chunk := f.read(8192):
                m.update(chunk)
        return m.hexdigest()

    def make_starboard_embed(self, message):
        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            description = f"{message.embeds[0].description}\n\n**[Click to jump to message!]({message.jump_url})**" if message.embeds[0].description is not nextcord.Embed.Empty else f"**[Click to jump to message!]({message.jump_url})**",
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar)
        embed.set_image(url=message.embeds[0].image.url)
        return embed

    def valid_embed(self, message):
        if (
            message.embeds is None
            or message.embeds[0].title is nextcord.Embed.Empty
            or message.embeds[0].description is nextcord.Embed.Empty
            or message.embeds[0].image is nextcord.Embed.Empty
        ):
            return False
        return True

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.guild is None
            or message.guild.id != 994266247577485473
            or not isinstance(nextcord.Member)
            or not message.author.bot
        ):
            return

        if message.author.id == 716390085896962058: # Poketwo
            if self.valid_embed(message):
                if "Guess the pokémon" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message)

                if "fled" in message.embeds[0].title and any(x in message.embeds[0].title.lower() for x in plasma.RARE_POKEMONS):
                    channel = message.guild.get_channel(994921306963316798)
                    i = 0

                    async for msg in message.channel.history(limit=30):
                        if self.valid_embed(msg):
                            i += 1
                            if i == 2:
                                embed = self.make_starboard_embed(msg)
                                await channel.send(f"<#{message.channel.id}>", embed=embed)
                                return

        if message.author.id == 669228505128501258: # Pokemon
            if self.valid_embed(message):
                if "Guess the pokémon" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message)

        if message.author.id == 705016654341472327: # Pokecord
            if self.valid_embed(message):
                if "Use" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message)

        if message.author.id == 704130818339242094: # Deriver
            if self.valid_embed(message):
                if "Guess the pokémon" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message)