from __future__ import annotations

__all__ = (
    "Emoji",
    "emoji"
)


class Emoji:
    def _get_emoji(id: int, *, animated: bool = False) -> Emoji:
        return f"<a:_:{id}>" if animated else f"<:_:{id}>"


    # Custom

    @classmethod
    def check(self) -> Emoji:
        return self._get_emoji(990273123444207636)

    @classmethod
    def cross(self) -> Emoji:
        return self._get_emoji(990273148379332678)


emoji = Emoji