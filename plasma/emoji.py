from __future__ import annotations

__all__ = (
    "Emoji",
    "Emote"
)


class Emoji:
    def __init__(self, id: int, *, animated: bool = False):
        if not isinstance(id, int):
            raise TypeError(f"Expected int parameter, received {id.__class__.__name__} instead.")

        if not isinstance(animated, bool):
            raise TypeError(f"Expected bool parameter, received {animated.__class__.__name__} instead.")

        self.id = id
        self.animated = animated

    def __repr__(self) -> str:
        return f"<Emoji id={self.id}>"

    def __str__(self) -> str:
        return f"<a:_:{self.id}>" if self.animated else f"<:_:{self.id}>"

    def __int__(self) -> int:
        return self.id

    def __hash__(self) -> int:
        return hash(self.id)

    @classmethod
    def check(self) -> Emoji:
        return str(Emoji(990273123444207636))

    @classmethod
    def cross(self) -> Emoji:
        return str(Emoji(990273148379332678))


Emote = Emoji