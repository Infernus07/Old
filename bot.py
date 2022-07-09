import plasma

import nextcord
from nextcord.ext import commands


class ClusterBot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            commands.when_mentioned_or("?", ">", "-"),
            activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Plasma"),
            allowed_mentions=nextcord.AllowedMentions(everyone=False),
            case_insensitive=True,
            intents=nextcord.Intents.all(),
            owner_ids=plasma.OWNERS
        )

        for i in plasma.COGS:
            self.load_extension(f"cogs.{i}")

        self.add_check(commands.guild_only())
        self.run("OTkwMjE3OTA2MzMzODM5NDcx.GfVsR3.4feXv_SN_rhcjTYycU58bxa0rO1okJYs80L-Lc")

    @property
    def mongo(self):
        return self.get_cog("Mongo")

    async def on_ready(self):
        print(f"Logged in as {self.user}")


if __name__ == "__main__":
    ClusterBot()