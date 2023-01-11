DGG-bot
=======

.. image:: https://img.shields.io/pypi/v/dgg-bot.svg
   :target: https://pypi.python.org/pypi/dgg-bot
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/dgg-bot.svg
   :target: https://pypi.python.org/pypi/dgg-bot
   :alt: PyPI supported Python versions

A library for making a bot in Destiny.gg chat.

Installing
----------

**Python 3.9 or higher is required** (version 0.5.0 and above, Python 3.8+ for versions below)

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U dgg-bot

    # Windows
    py -3 -m pip install -U dgg-bot


Usage
-----

Not sure what to put here at this point in time. Unauthorized chat bots are subject to being **banned**, ask Cake in DGG for permission and guidelines for chat bots before running one.


Examples
--------

A simple bot with three commands and will yump back at chatters.

.. code-block:: python

    from dggbot import DGGBot
    import time

    bot = DGGBot(
        "AUTH_TOKEN",
        username="Username",
        owner="Owner",
        prefix="$"
    )  # default command prefix is "!"

    @bot.command()
    @bot.is_owner()  # only the owner named above can use this command.
    def test(msg):  # $test
        msg.reply("Test 123")

    @bot.command(aliases=["banmeplease"])  # aliases for this command
    def banme(msg):  # $banme / $banmeplease
        bot.send("RightToBearArmsLOL BINGQILIN nathanTiny2")


    def is_cake(msg):  # a check where only the user Cake can use commands with this check
        return msg.nick == "Cake"

    @bot.command(aliases=["oooo"])
    @bot.check(is_cake)
    def pog(msg):
        msg.reply("Cake OOOO")

    """
    Events
    You can either name the function after the event, or include the event name in the decorator.
    mention() is also included as a shortcut for event("on_mention").

    Event names: on_ban, on_broadcast, on_join, on_mention, on_msg, on_mute, on_privmsg, on_quit,
                 on_refresh, on_unban
    """

    @bot.event()
    def on_msg(msg):
        print(msg)

    # @bot.event("on_mention")
    @bot.mention()
    def yump(msg):
        if "MiyanoHype" in msg.data:
            time.sleep(0.5)
            msg.reply(f"{msg.nick} MiyanoHype")

    if __name__ == "__main__":
        while True:
            bot.run()
            time.sleep(2)


Connecting to alternative DGG environments.

.. code-block:: python

    from dggbot import DGGBot
    import time

    bot = DGGBot(
        "AUTH_TOKEN",
        username="Username",
        owner="Owner",
        prefix="$",
        wss="wss://chat.omniliberal.dev/ws",
    )

    @bot.event()
    def on_msg(msg):
        print(msg)

    if __name__ == "__main__":
        while True:
            bot.run(origin="https://www.omniliberal.dev")
            time.sleep(2)