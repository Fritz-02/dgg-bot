"""
Colorful chat in console, with messages, greentext, subscriber colors, flair names, broadcast messages,
and when chatters join and left chat.
"""
from dggbot import DGGChat, Message
import itertools

# Option(s) for what messages appear or not
JOIN_AND_LEFT = True


class ANSI:
    T1_COLOR = "\033[94m"
    T2_COLOR = "\033[96m"
    T3_COLOR = "\033[32m"
    T4_COLOR = "\033[95m"
    T5_COLOR = "\033[35m"
    BROADCAST = "\033[33m"
    RESET_COLOR = "\033[39m"
    GREENTEXT = "\033[32m"


def bold(text: str) -> str:
    return f"\033[1m{text}\033[22m"


def rainbowify(text: str, previous_color: str = ANSI.RESET_COLOR) -> str:
    colors = ["\033[3{}m{{}}\033[39m".format(n) for n in range(1, 7)]
    rainbow = itertools.cycle(colors)
    letters = [next(rainbow).format(L) for L in text]
    return "".join(letters) + previous_color


chat = DGGChat()
tier1 = chat.get_flair("flair13")
tier2 = chat.get_flair("flair1")
tier3 = chat.get_flair("flair3")
tier4 = chat.get_flair("flair8")
tier5 = chat.get_flair("flair42")


def get_flair_str(msg: Message) -> str:
    flair_str = "|".join(
        flair.label.replace("Subscriber ", "").replace("Tier ", "T")
        for flair in msg.features
        if flair.label not in ("Subscriber",)
    )
    return f" [{flair_str}]" if flair_str else ""


if JOIN_AND_LEFT:

    @chat.event()
    def on_join(msg):
        print(
            f"[{msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]{get_flair_str(msg)} {bold(msg.nick)} has joined.\033[0m"
        )

    @chat.event()
    def on_quit(msg):
        print(
            f"[{msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]{get_flair_str(msg)} {bold(msg.nick)} left chat.\033[0m"
        )


@chat.event()
def on_broadcast(msg):
    print(
        f"{ANSI.BROADCAST}[{msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {msg.data}\033[0m"
    )


@chat.event()
def on_msg(msg: Message):
    color = ""
    nick = msg.nick

    if tier1 in msg.features:
        color = ANSI.T1_COLOR
    elif tier2 in msg.features:
        color = ANSI.T2_COLOR
    elif tier3 in msg.features:
        color = ANSI.T3_COLOR
    elif tier4 in msg.features:
        color = ANSI.T4_COLOR
    elif tier5 in msg.features:
        color = ANSI.T5_COLOR
        nick = rainbowify(nick, color)

    data = msg.data
    if data.startswith(">"):
        data = ANSI.GREENTEXT + data

    print(
        f"{color}[{msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}]{get_flair_str(msg)} {bold(nick)}: {ANSI.RESET_COLOR}{data}\033[0m"
    )


chat.run_forever()
