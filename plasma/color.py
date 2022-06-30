from __future__ import annotations
import colorsys
import random

__all__ = (
    "Color",
    "Colour"
)


class Color:
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f"Expected int parameter, received {value.__class__.__name__} instead.")

        self.value = value

    def _get_byte(self, byte: int) -> int:
        return (self.value >> (8 * byte)) & 0xFF

    def __repr__(self) -> str:
        return f"<Colour value={self.value}>"

    def __str__(self) -> str:
        return f"#{self.value:0>6x}"

    def __int__(self) -> int:
        return self.value

    def __hash__(self) -> int:
        return hash(self.value)

    @property
    def r(self) -> int:
        return self._get_byte(2)

    @property
    def g(self) -> int:
        return self._get_byte(1)

    @property
    def b(self) -> int:
        return self._get_byte(0)

    @classmethod
    def from_rgb(self, r: int, g: int, b: int) -> Color:
        return int(Color((r << 16) + (g << 8) + b))

    @classmethod
    def from_hsv(self, h: float, s: float, v: float) -> Color:
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return self.from_rgb(*(int(x * 255) for x in rgb))

    @classmethod
    def default(self) -> Color:
        return int(Color(0))

    @classmethod
    def random(self) -> Color:
        return self.from_hsv(random.random(), 1, 1)

    @classmethod
    def blue(self) -> Color:
        return int(Color(0x3498DB))

    @classmethod
    def blurple(self) -> Color:
        return int(Color(0x5865F2))

    @classmethod
    def dark_theme(self) -> Color:
        return int(Color(0x36393F))

    @classmethod
    def gold(self) -> Color:
        return int(Color(0xF1C40F))

    @classmethod
    def green(self) -> Color:
        return int(Color(0x2ECC71))

    @classmethod
    def greyple(self) -> Color:
        return int(Color(0x99AAB5))

    @classmethod
    def magenta(self) -> Color:
        return int(Color(0xE91E63))

    @classmethod
    def og_blurple(self) -> Color:
        return int(Color(0x7289DA))

    @classmethod
    def orange(self) -> Color:
        return int(Color(0xE67E22))

    @classmethod
    def purple(self) -> Color:
        return int(Color(0x9B59B6))

    @classmethod
    def red(self) -> Color:
        return int(Color(0xE74C3C))

    @classmethod
    def teal(self) -> Color:
        return int(Color(0x1ABC9C))

    @classmethod
    def yellow(self) -> Color:
        return int(Color(0xFEE75C))

    @classmethod
    def amaranth(self) -> Color:
        return int(Color(0xe52b50))

    @classmethod
    def blush(self) -> Color:
        return int(Color(0xe69296))

    @classmethod
    def fuchsia(self) -> Color:
        return int(Color(0xff00ff))

    @classmethod
    def ice(self) -> Color:
        return int(Color(0xbddeec))

    @classmethod
    def indigo(self) -> Color:
        return int(Color(0x726eff))

    @classmethod
    def lilac(self) -> Color:
        return int(Color(0xc8a2c8))

    @classmethod
    def lime(self) -> Color:
        return int(Color(0xb7ff00))

    @classmethod
    def midnight(self) -> Color:
        return int(Color(0x007bff))

    @classmethod
    def obsidian(self) -> Color:
        return int(Color(0x010101))

    @classmethod
    def sky(self) -> Color:
        return int(Color(0x00c8ff))

    @classmethod
    def snow(self) -> Color:
        return int(Color(0xa4cce4))

    @classmethod
    def tangerine(self) -> Color:
        return int(Color(0xef8e38))


Colour = Color