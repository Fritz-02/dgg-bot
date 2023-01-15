from dggbot import DGGBot
import time

bot = DGGBot(
    username="Bot",
    owner="Owner",
    wss="wss://chat.omniliberal.dev/ws",
    sid="SID",
)


# Command arguments
@bot.command()
def hug(msg, arg: str):
    """Hugs whatever is typed after the command, or the user calling it."""
    msg.reply(f"TeddyPepe {arg if arg else msg.nick} TeddyPepe")


@bot.command()
def logs(msg, username: str = None):
    """Link logs of given username, or command user's."""
    if not username:
        username = msg.nick
    elif " " in username:
        username = username.split(" ")[0]
    msg.reply(f"https://rustlesearch.dev/?username={username}&channel=Destinygg")


# Custom command permissions
def is_cake(msg):
    """A check where only the user 'Cake' can use commands with this check"""
    return msg.nick == "Cake"


@bot.command()
@bot.check(is_cake)
def cake(msg):
    """Command can only be used by the user 'Cake'"""
    msg.reply("🎂")


while True:
    bot.run(origin="https://www.omniliberal.dev")
    time.sleep(2)
