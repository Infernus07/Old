from datetime import datetime

import nextcord

from .yaml import color, emoji

__all__ = (
    "Embed",
)


class Embed(nextcord.Embed):
    def __init__(
        self,
        *,
        colour: int = color["BLUE"],
        title: str = nextcord.Embed.Empty,
        description: str = nextcord.Embed.Empty,
        timestamp: datetime | bool = None,
        mode: str = None
    ):
        if mode is not None:
            colour = color["GREEN"] if mode == "check" else color["AMARANTH"]
            description = emoji[mode.upper()] + " " + description

        timestamp = timestamp if timestamp is not True else datetime.utcnow()
        super().__init__(colour=colour, title=title, description=description, timestamp=timestamp)