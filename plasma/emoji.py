from __future__ import annotations

__all__ = ("Emoji",)


class Emoji:
    def __init__(self, id, *, animated=False):
        self.id = id
        self.animated = animated

    def __repr__(self):
        return f"<a:_:{self.id}>" if self.animated else f"<:_:{self.id}>"

    
    # Colors

    @classmethod
    def amaranth(self):
        return Emoji(995599005427978250)

    @classmethod
    def blush(self):
        return Emoji(995598969898020914)

    @classmethod
    def fuchsia(self):
        return Emoji(995598531027017820)

    @classmethod
    def ice(self):
        return Emoji(995598443659669595)

    @classmethod
    def indigo(self):
        return Emoji(995597795329327164)

    @classmethod
    def lilac(self):
        return Emoji(995597738123210762)

    @classmethod
    def lime(self):
        return Emoji(995597665196855316)

    @classmethod
    def midnight(self):
        return Emoji(995597342235443240)

    @classmethod
    def obsidian(self):
        return Emoji(995597290792296483)

    @classmethod
    def sky(self):
        return Emoji(995597096499556362)

    @classmethod
    def snow(self):
        return Emoji(995596623625338900)

    @classmethod
    def tangerine(self):
        return Emoji(995596559490232370)


    # Bots

    @classmethod
    def poketwo(self):
        return Emoji(995599343253979186)

    @classmethod
    def pokemon(self):
        return Emoji(995599282184925224)

    @classmethod
    def pokecord(self):
        return Emoji(995599109945839687)

    @classmethod
    def deriver(self):
        return Emoji(995599063259025458)

    
    # Utils

    @classmethod
    def check(self):
        return Emoji(995599490968985600)

    @classmethod
    def cross(self):
        return Emoji(995599463961853962)

    @classmethod
    def red_tick(self):
        return Emoji(995243875906097252, animated=True)