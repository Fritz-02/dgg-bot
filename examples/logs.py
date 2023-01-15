from dggbot import DGGChat, Message
import time


chat = DGGChat()  # no auth_token is needed when you only need to read chat


def write_to_file(msg: Message):
    """Write to file or database to store logs."""
    return NotImplemented


@chat.event()
def on_msg(msg):
    """Write the message to a file or database."""
    write_to_file(msg)


while True:
    # Connect back to chat when disconnected after 2 seconds.
    chat.run()
    time.sleep(2)
