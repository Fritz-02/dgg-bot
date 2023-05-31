from dggbot import DGGBot
from dggbot.message import Message, PollMessage

bot = DGGBot("auth_token")


@bot.event()
def on_pollstart(poll: PollMessage):
    """Automatically vote YEE in every poll"""
    if "YEE" in poll.options:
        poll.vote(poll.options.index("YEE") + 1)


@bot.command()
def vote(msg: Message):
    """Vote for the first option in a poll"""
    bot.cast_vote(1)


@bot.event()
def on_pollstop(poll: PollMessage):
    """Grab the results of a poll"""
    print(dict(zip(poll.options, poll.totals)))


if __name__ == "__main__":
    bot.run_forever()
