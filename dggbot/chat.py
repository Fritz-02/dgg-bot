import json
import logging
from typing import Union
import websocket

from .event import EventType
from .message import Message, PrivateMessage
from .errors import Throttled


class DGGChat:
    WSS = "wss://chat.destiny.gg/ws"
    URL = "https://www.destiny.gg"

    def __init__(self, auth_token=None, *, username: str = None):
        self.username = username.lower()
        self.ws = websocket.WebSocketApp(self.WSS, cookie=f'authtoken={auth_token}' if auth_token else None, on_open=self._on_open, on_message=self._on_message, on_error=self._on_error, on_close=self._on_close)
        self._connected = False

    def is_mentioned(self, msg: Union[Message, PrivateMessage]) -> bool:
        return False if self.username is None else (self.username in msg.data.lower())

    def on_mention(self, msg):
        """Do stuff when mentioned."""
        pass

    def on_broadcast(self, msg):
        """Do stuff when a BROADCAST is received."""
        pass

    def on_join(self, msg):
        """Do stuff when chatter joins."""
        pass

    def on_quit(self, msg):
        """Do stuff when chatter joins."""
        pass

    def on_msg(self, msg):
        """Do stuff when a MSG is received."""
        pass

    def on_privmsg(self, msg):
        """Do stuff when a PRIVMSG is received."""
        pass

    def _on_message(self, ws, message: str):
        event_type, data = message.split(maxsplit=1)
        data = json.loads(data)
        if event_type == EventType.MESSAGE:
            msg = Message(event_type, data['nick'], data['features'], data['timestamp'], data['data'])
            logging.debug(msg)
            self.on_msg(msg)
            if self.is_mentioned(msg):
                self.on_mention(msg)
        elif event_type == EventType.PRIVMSG:
            msg = PrivateMessage(event_type, data['nick'], data['features'], data['timestamp'], data['data'], data['messageid'])
            logging.debug(msg)
            self.on_privmsg(msg)
            if self.is_mentioned(msg):
                self.on_mention(msg)
        elif event_type == EventType.BROADCAST:
            msg = Message(event_type, timestamp=data['timestamp'], data=data['data'])
            logging.debug(msg)
            self.on_broadcast(msg)
        elif event_type == EventType.NAMES:
            logging.debug(event_type, data)
        elif event_type in (EventType.JOIN, EventType.QUIT):
            msg = Message(event_type, data['nick'], data['features'], data['timestamp'])
            logging.debug(msg)
            if event_type == EventType.JOIN:
                self.on_join(msg)
            else:
                self.on_quit(msg)
        elif event_type == EventType.MUTE:
            msg = Message(event_type, data['nick'], timestamp=data['timestamp'],
                          data=f"{data['data']} muted by {data['nick']} for {data.get('duration', 'N/A')}.")
            logging.debug(msg)
        elif event_type == EventType.ERROR:
            if data['description'] == 'throttled':
                raise Throttled
            else:
                logging.error(event_type, data)
                raise Exception(data['description'])
        else:
            logging.warning(f'Unknown event type: {event_type} {data}')

    def _on_open(self, ws):
        logging.info(f'Connecting to: {self.WSS}')
        self._connected = True

    def _on_close(self, ws, *_):
        logging.debug(f'Connection closed.')
        self._connected = False

    def _on_error(self, ws, error):
        logging.error(error)

    def run(self):
        self.ws.run_forever(origin=self.URL)

    def send(self, msg: str):
        payload = {'data': msg}
        self.ws.send(f'MSG {json.dumps(payload)}')
