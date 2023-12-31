from functools import cache


class EventType:
    BAN = "BAN"
    BROADCAST = "BROADCAST"
    DEATH = "DEATH"
    DONATION = "DONATION"
    ERROR = "ERR"
    GIFTSUB = "GIFTSUB"
    JOIN = "JOIN"
    MASSGIFT = "MASSGIFT"
    ME = "ME"
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
    SUBSCRIPTION = "SUBSCRIPTION"
    UNBAN = "UNBAN"
    UNMUTE = "UNMUTE"
    UPDATEUSER = "UPDATEUSER"
    VOTECAST = "VOTECAST"

    @classmethod
    @cache
    def types(cls) -> tuple[str]:
        return tuple(v for k, v in cls.__dict__.items() if k.isupper())
