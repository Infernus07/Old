from .views import Confirmation

__all__ = (
    "get_confirmation",
)


async def get_confirmation(ctx, message):
    view = Confirmation(ctx)
    view.message = await ctx.channel.send(message, view=view)
    await view.wait()
    return view.result