from functools import cache


class EventType:
    BAN = "BAN"
    BROADCAST = "BROADCAST"
    ERROR = "ERR"
    JOIN = "JOIN"
    MESSAGE = "MSG"
    MUTE = "MUTE"
    NAMES = "NAMES"
    PIN = "PIN"
    POLLSTART = "POLLSTART"
    POLLSTOP = "POLLSTOP"
    PRIVMSG = "PRIVMSG"
    PRIVMSGSENT = "PRIVMSGSENT"
    QUIT = "QUIT"
    REFRESH = "REFRESH"
    SUBONLY = "SUBONLY"
    UNBAN = "UNBAN"
    UNMUTE = "UNMUTE"
    VOTECAST = "VOTECAST"

    @classmethod
    @cache
    def types(cls) -> tuple[str]:
        return tuple(v for k, v in cls.__dict__.items() if k.isupper())
