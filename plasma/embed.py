import datetime
import nextcord
from typing import Literal

from .color import Color
from .emoji import Emoji

__all__ = (
    "Embed",
)

Mode = Literal["G", "R"]


class Embed(nextcord.Embed):
    def __init__(
        self,
        description: str = nextcord.Embed.Empty,
        *,
        color: int = Color.blue(),
        title: str = nextcord.Embed.Empty,
        timestamp: datetime.datetime | bool = None,
        mode: Mode = None
    ):
        self.description = description
        self.mode = mode

        if mode is not None:
            color, description = self._get_mode_values()

        timestamp = timestamp if timestamp is not True else datetime.datetime.utcnow()
        super().__init__(color=color, title=title, description=description, timestamp=timestamp)

    def _get_mode_values(self) -> tuple[Color, str]:
        if self.mode == "G":
            return Color.green(), Emoji.check() + " " + self.description

        if self.mode == "R":
            return Color.red(), Emoji.cross() + " " + self.description