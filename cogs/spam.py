import itertools
import random
import requests
import string

from nextcord.ext import commands, tasks


SPAMMERS = (
    "OTIxNDAwNDQ1MjMzMTQzODIw.Yb70XQ._qJ8dVFvLV6pWLYWg1gvZwYhNV0", # Jiya
    "OTIxMDI2NDAyMjMxNDEwNjk4.YbtajA.Iy48q-yVbLn8s2z1224ZNBYLyNo", # May
    "OTIxNjEyMjY2ODIxMDE3NjMw.Yb71MA.uQU0WFl3e4iqgyareidLTivIRDM", # Serena
    "ODg5MDg0MjA2Njc0NzQ3Mzky.YdK5dw.aBvdLbIpvrdyasCMi3xdcNYtF6Y"  # Tyson
)

class Spam(commands.Cog):
    """For spam."""

    def __init__(self, bot):
        self.bot = bot
        self.spammers = itertools.cycle(SPAMMERS)
        self.spam.start()

    @tasks.loop(seconds=0.5)
    async def spam(self):
        requests.post(
            "https://discord.com/api/v9/channels/994922903105720330/messages",
            {"content": "".join(random.choices(string.ascii_letters, k=1))},
            headers={"authorization": next(self.spammers)}
        )

    @spam.before_loop
    async def before_spam(self):
        await self.bot.wait_until_ready()

    async def cog_unload(self):
        self.spam.cancel()

def setup(bot):
    bot.add_cog(Spam(bot))