from datetime import datetime
import nextcord
from typing import Literal

from .color import Color
from .emoji import Emoji

__all__ = (
    "Embed",
)

Mode = Literal["check", "cross"]
Empty = nextcord.Embed.Empty


class Embed(nextcord.Embed):
    def __init__(
        self,
        description: str = Empty,
        *,
        color: int = Color.blue(),
        title: str = Empty,
        timestamp: datetime | bool = None,
        mode: Mode = None
    ):
        if mode is not None:
            color, description = self._get_mode_values(description, mode)

        timestamp = timestamp if timestamp is not True else datetime.utcnow()
        super().__init__(color=color, title=title, description=description, timestamp=timestamp)

    def _get_mode_values(self, description: str, mode: Mode) -> tuple[Color, str]:
        if mode == "check":
            return Color.green(), Emoji.check() + " " + description

        if mode == "cross":
            return Color.amaranth(), Emoji.cross() + " " + description