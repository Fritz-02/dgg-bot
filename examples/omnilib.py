from dggbot import DGGChat


cfg = {
    "wss": "wss://chat.omniliberal.dev/ws",
    "wss-origin": "https://www.omniliberal.dev",
    "baseurl": "https://www.omniliberal.dev",
    "endpoints": {"user": "/api/chat/me", "userinfo": "/api/userinfo"},
    "flairs": "https://cdn.omniliberal.dev/flairs/flairs.json",
}

# Can also load config from file
# cfg = "../configs/omnilibconfig.json"

chat = DGGChat(config=cfg)


@chat.event()
def on_msg(msg):
    print(msg)


chat.run_forever()
