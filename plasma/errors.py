class DiscordException(Exception):
    pass


class CommandError(DiscordException):
    def __init__(self, message=None, *args):
        if message is not None:
            m = message.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")
            super().__init__(m, *args)
        else:
            super().__init__(*args)


class NotInGuild(CommandError):
    pass