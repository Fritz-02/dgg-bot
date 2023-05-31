from dggbot import DGGChat, Message

chat = DGGChat()  # no auth_token is needed when you only need to read chat


def write_to_file(msg: Message):
    """Write to file or database to store logs."""
    return NotImplemented


@chat.event()
def on_msg(msg):
    """Write the message to a file or database."""
    write_to_file(msg)


chat.run_forever()
