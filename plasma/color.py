from __future__ import annotations
import colorsys
import random

__all__ = (
    "Color",
    "color"
)


class Color:
    def _get_color(value: int) -> Color:
        return value

    @classmethod
    def from_rgb(self, r: int, g: int, b: int) -> Color:
        return self._get_color((r << 16) + (g << 8) + b)

    @classmethod
    def from_hsv(self, h: float, s: float, v: float) -> Color:
        rgb = colorsys.hsv_to_rgb(h, s, v)
        return self.from_rgb(*(int(x * 255) for x in rgb))

    @classmethod
    def default(self) -> Color:
        return self._get_color(0)

    @classmethod
    def random(self) -> Color:
        return self.from_hsv(random.random(), 1, 1)


    # Default

    @classmethod
    def blue(self) -> Color:
        return self._get_color()

    @classmethod
    def blurple(self) -> Color:
        return self._get_color()

    @classmethod
    def dark_theme(self) -> Color:
        return self._get_color()

    @classmethod
    def gold(self) -> Color:
        return self._get_color()

    @classmethod
    def green(self) -> Color:
        return self._get_color()

    @classmethod
    def greyple(self) -> Color:
        return self._get_color()

    @classmethod
    def magenta(self) -> Color:
        return self._get_color()

    @classmethod
    def og_blurple(self) -> Color:
        return self._get_color()

    @classmethod
    def orange(self) -> Color:
        return self._get_color()

    @classmethod
    def purple(self) -> Color:
        return self._get_color()

    @classmethod
    def red(self) -> Color:
        return self._get_color()

    @classmethod
    def teal(self) -> Color:
        return self._get_color()

    @classmethod
    def yellow(self) -> Color:
        return self._get_color()


    # Custom

    @classmethod
    def amaranth(self) -> Color:
        return self._get_color()

    @classmethod
    def blush(self) -> Color:
        return self._get_color()

    @classmethod
    def fuchsia(self) -> Color:
        return self._get_color()

    @classmethod
    def ice(self) -> Color:
        return self._get_color()

    @classmethod
    def indigo(self) -> Color:
        return self._get_color()

    @classmethod
    def lilac(self) -> Color:
        return self._get_color()

    @classmethod
    def lime(self) -> Color:
        return self._get_color()

    @classmethod
    def midnight(self) -> Color:
        return self._get_color()

    @classmethod
    def obsidian(self) -> Color:
        return self._get_color()

    @classmethod
    def sky(self) -> Color:
        return self._get_color()

    @classmethod
    def snow(self) -> Color:
        return self._get_color()

    @classmethod
    def tangerine(self) -> Color:
        return self._get_color()


color = Color