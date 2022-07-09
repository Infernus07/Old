from .errors import *
from .views import *


async def get_confirmation(ctx, message):
    view = Confirmation(ctx)
    view.message = await ctx.channel.send(message, view=view)
    await view.wait()
    return view.result