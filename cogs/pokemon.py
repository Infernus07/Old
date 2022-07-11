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

    def get_hash(self, image):
        m = hashlib.md5()
        with open(image, "rb") as f:
            while chunk := f.read(8192):
                m.update(chunk)
        return m.hexdigest()

    def make_starboard_embed(self, message):
        if message.embeds is not None:
            embed = nextcord.Embed(
                color=nextcord.Color.blue(),
                description = f"{message.embeds[0].description}\n\n**[Click to jump to message!]({message.jump_url})**" if message.embeds[0].description is not nextcord.Embed.Empty else f"**[Click to jump to message!]({message.jump_url})**",
                timestamp=datetime.utcnow()
            )
            embed.set_author(name=message.author.name, icon_url=message.author.avatar)
            embed.set_image(url=message.embeds[0].image.url)
            return embed

        embed = nextcord.Embed(
            color=nextcord.Color.blue(),
            description=message.content,
            timestamp=datetime.utcnow()
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar)
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

        if (
            (message.author.id == 716390085896962058 and message.content.startswith("The pokémon is")) # Poketwo
            or (message.author.id == 669228505128501258 and message.content.startswith("The wild pokémon is")) # Pokemon
            or (message.author.id == 704130818339242094 and message.content.startswith("Hint")) # Deriver
        ):
            self.bot.dispatch("hint", message)
            return

        if message.author.id == 716390085896962058 and "You" in message.content: # Poketwo
            data = message.content[message.content.find("You"):]
            channel = message.guild.get_channel(994921306963316798)

            if "caught" in data and not any(x in data for x in ("evolve", "purchase", "select")):
                if "These colors seem unusual..." in data:
                    with suppress(nextcord.HTTPException, nextcord.NotFound):
                        await message.pin()
                    embed = self.make_starboard_embed(message)
                    await channel.send(f"<#{message.channel.id}>", embed=embed)
                    return

                if any(x in data.lower() for x in plasma.RARE_POKEMONS):
                    async for msg in message.channel.history(limit=30):
                        if self.valid_embed(msg):
                            embed = self.make_starboard_embed(msg)
                            await channel.send(f"<#{message.channel.id}>", embed=embed)
                            return

        if message.author.id == 669228505128501258 and "you" in message.content: # Pokemon
            data = message.content[message.content.find("you"):]
            channel = message.guild.get_channel(994923221038157906)

            if "caught" in data and not any(x in data for x in ("evolve", "purchase", "select")):
                if "Shiny" in data:
                    with suppress(nextcord.HTTPException, nextcord.NotFound):
                        await message.pin()
                    embed = self.make_starboard_embed(message)
                    await channel.send(f"<#{message.channel.id}>", embed=embed)
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
                    self.bot.dispatch("spawn", message, "pokemon", 994923221038157906, 994960527287668826)

        if message.author.id == 705016654341472327: # Pokecord
            if self.valid_embed(message):
                if "Use" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message, "pokecord", 994923747893063700, 994960678366494782)

        if message.author.id == 704130818339242094: # Deriver
            if self.valid_embed(message):
                if "Guess the pokémon" in message.embeds[0].description:
                    self.bot.dispatch("spawn", message, "deriver", 994924224089169931, 994960742103142420)

    @commands.Cog.listener()
    async def on_hint(self, message):
        choices = []
        check = None

        if message.author.id == 716390085896962058: # Poketwo
            hint = message.content.replace("\_", "_").replace("The pokémon is ", "").replace(" ", "_").lower()[:-1]
        elif message.author.id == 669228505128501258: # Pokemon
            hint = message.content.replace("\_", "_").replace("The wild pokémon is ", "").replace(" ", "_").lower()
        elif message.author.id == 704130818339242094: # Deriver
            hint = message.content.replace("\_", "_").replace("Hint: ", "").replace("`", "").replace(" ", "_").lower()

        for pokemon in plasma.POKEMONS:
            if len(pokemon) == len(hint):
                for i in range(len(pokemon)):
                    if hint[i] != "_":
                        if pokemon[i] == hint[i]:
                            check = True
                        else:
                            check = False
                            break
                
                if check:
                    choices.append(plasma.title(pokemon))

        if len(choices) > 0:
            await message.channel.send("> **" + ", ".join(choices) + "**")

    @commands.Cog.listener()
    async def on_spawn(self, message, name, channel_id, role_id):
        async with self.session.get(message.embeds[0].image.url) as f:
            Image.open(io.BytesIO(await f.read())).save(f"assets/{name}.png")

        hash = self.get_hash(f"assets/{name}.png")
        doc = self.col.find_one({"hash": hash})
        rarity = ("legendary", "mythical", "ultra beast", "event", "other") if message.author.id != 705016654341472327 else ("legendary", "mythical", "event", "other")

        if doc is None:
            doc = self.col.find_one({"hashes": hash})

        if doc is not None:
            channel = message.guild.get_channel(channel_id)

            if any(x == doc["rarity"] for x in rarity):
                role = message.guild.get_role(role_id)
                await message.channel.send(f"{role.mention} Look it could be a **{plasma.title(doc['name'])}**.")

                embed = self.make_starboard_embed(message)
                await channel.send(f"<#{message.channel.id}>", embed=embed)

            hunter = list(self.col.find({name: doc["name"]}))
            if len(hunter) > 0:
                hunters = " ".join(f"<@{hunter['_id']}>")
                await message.channel.send(f"**{plasma.title(doc['name'])}:** {hunters}")