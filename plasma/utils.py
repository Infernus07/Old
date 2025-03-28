import nextcord

from .views import Confirmation

__all__ = ("FakeUser", "sub", "title", "profanity_words", "get_confirmation")

NON_TRIGGER_WORDS = (
    "hoenn",
    "fukano"
)


class FakeUser(nextcord.Object):
    def __str__(self):
        return str(self.id)

    @property
    def display_avatar(self):
        return "https://cdn.discordapp.com/embed/avatars/0.png"

    @property
    def mention(self):
        return "<@{0.id}>".format(self)


def sub(text, words):
    for i in words:
        text = text.replace(i, "")
    return text.strip()


def title(text):
    text = " ".join(x.capitalize() for x in text.split())
    text = text.replace("Ho-oh", "Ho-Oh")
    return text

def profanity_words(text):
    words = sub(text.lower(), NON_TRIGGER_WORDS)
    return words


async def get_confirmation(ctx, message):
    view = Confirmation(ctx)
    view.message = await ctx.send(message, view=view)
    await view.wait()
    return view.result