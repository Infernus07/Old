from collections import defaultdict
import itertools
import textwrap

from nextcord.ext import commands, tasks


class Post:
    def __init__(self, channels, message, *, each=1):
        self.channels = itertools.cycle(channels)
        self.do_post = itertools.cycle([True] + [False] * (each - 1))
        self.message = textwrap.dedent(message).strip()


POSTS = [
    Post(
        [994921158589829181],
        """
        **Reminder:** Get access roles from <#995006311391567983> to get access to various channels.
        """
    ),
    Post(
        [994921338017947661],
        """
        **Reminder:** This channel is for shiny hunters.

        • You need to ping for the shiny hunters once a pokemon spawns.
        • You can catch the pokemon once the timer ran out.
        • Legendary / Mythical / Ultra Beast / Alolan / Galarian / Hisuian pokemons are ffa.
        • All 2nd & 3rd stage pokemons are ffa excluding the evolutions of baby pokemons.
        • You also need to ping for event pokemons.
        """
    )
]


class AutoPost(commands.Cog):
    """For auto post."""

    def __init__(self, bot):
        self.bot = bot
        self.updated = defaultdict(bool)
        self.autopost.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.guild is None
            or message.guild.id != 994266247577485473
            or message.author == self.bot.user
        ):
            return

        self.updated[message.channel.id] = True

    @tasks.loop(minutes=5)
    async def autopost(self):
        for post in POSTS:
            if not next(post.do_post):
                continue

            channel_id = next(post.channels)
            if self.updated[channel_id]:
                channel = self.bot.get_channel(channel_id)
                await channel.send(post.message)
                self.updated[channel_id] = False

    @autopost.before_loop
    async def before_autopost(self):
        await self.bot.wait_until_ready()

    async def cog_unload(self):
        self.autopost.cancel()

def setup(bot):
    bot.add_cog(AutoPost(bot))