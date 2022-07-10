from .views import Confirmation

__all__ = ("sub", "title", "get_confirmation")


def sub(text, words):
    for i in words:
        text = text.replace(i, "")
    return text.strip()


def title(text):
    text = " ".join(x.capitalize() for x in text.split())
    text = text.replace("Ho-oh", "Ho-Oh")
    return text


async def get_confirmation(ctx, message):
    view = Confirmation(ctx)
    view.message = await ctx.send(message, view=view)
    await view.wait()
    return view.result