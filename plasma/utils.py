from .views import Confirmation

__all__ = (
    "get_confirmation",
    "sub"
)


async def get_confirmation(ctx, message):
    view = Confirmation(ctx)
    view.message = await ctx.channel.send(message, view=view)
    await view.wait()
    return view.result

def sub(text, words):
    for i in words:
        text = text.replace(i, "")
    return text.strip()