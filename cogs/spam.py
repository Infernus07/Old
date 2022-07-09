import itertools
import random
import requests
import string

from nextcord.ext import commands, tasks


class Spammer:
    def __init__(self, channel_id, token, message=None):
        self.channel_id = channel_id
        self.token = token
        self.message = message


SPAMMERS = [
    Spammer(994922903105720330, "OTIxNDAwNDQ1MjMzMTQzODIw.Yb70XQ._qJ8dVFvLV6pWLYWg1gvZwYhNV0"), # Jiya
    Spammer(994922903105720330, "OTIxMDI2NDAyMjMxNDEwNjk4.YbtajA.Iy48q-yVbLn8s2z1224ZNBYLyNo"), # May
    Spammer(994922903105720330, "OTIxNjEyMjY2ODIxMDE3NjMw.Yb71MA.uQU0WFl3e4iqgyareidLTivIRDM"), # Serena
    Spammer(994922903105720330, "ODg5MDg0MjA2Njc0NzQ3Mzky.YdK5dw.aBvdLbIpvrdyasCMi3xdcNYtF6Y"), # Tyson
    Spammer(994922903105720330, "OTcyODM4MzUxMzUyNzc0Njk2.GCVfE8.-ClXeJkJlNL8DPRKNd_wwdqwGjPtdRzjju1YyU"), # Touka 1
    Spammer(994922903105720330, "OTczMjUwMjg4MTU4OTA0NDEx.Ynk4Ig.QTvzSmW6YjXAOLY1vM2BQSK-v8M") # Touka 2
]


class Spam(commands.Cog):
    """For spam."""

    def __init__(self, bot):
        self.bot = bot
        self.spammers = itertools.cycle(SPAMMERS)
        self.spam.start()

    @tasks.loop(seconds=0.5)
    async def spam(self):
        spammer = next(self.spammers)
        message = spammer.message or "".join(random.choices(string.ascii_letters, k=1))

        requests.post(f"https://discord.com/api/v9/channels/{spammer.channel_id}/messages", {"content": message}, headers={"authorization": spammer.token})

    @spam.before_loop
    async def before_spam(self):
        await self.bot.wait_until_ready()

    async def cog_unload(self):
        self.spam.cancel()

def setup(bot):
    bot.add_cog(Spam(bot))