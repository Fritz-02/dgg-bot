from dggbot import DGGBot

bot = DGGBot("AUTH_TOKEN", owner="Owner")


@bot.command()
def ping(msg):
    msg.reply("Pong")


# Aliases
@bot.command(aliases=["obamna"])
def twitter(msg):
    """Replies with the following message. Aliases are optional, the function name is the same as the command name."""
    msg.reply("#youtube/tZ_gn0E87Qo LULW")


# Owner-only commands
@bot.command()
@bot.is_owner()
def test(msg):
    """Test command that is restricted to only the bot owner."""
    msg.reply("Test 123")


bot.run_forever()
