from typing import Type, Tuple, Dict
import time
from attr import dataclass
from mautrix.types import EventType, MessageType, UserID, RoomID
from mautrix.util.config import BaseProxyConfig
from maubot import Plugin, MessageEvent
from maubot.handlers import event
from .config import Config, ConfigError

@dataclass
class HelloBot(Plugin):
  allowed_msgtypes: Tuple[MessageType, ...] = (MessageType.TEXT, MessageType.EMOTE)
  @classmethod
  def get_config_class(cls) -> Type[BaseProxyConfig]:
    return Config
  async def start(self) -> None:
    await super().start()
    self.on_external_config_update()
  def on_external_config_update(self) -> None:
    self.config.load_and_update()
    try:
      self.config.parse_data()
    except ConfigError:
      self.log.exception("Failed!")
  @event.on(EventType.ROOM_MEMBER)
  async def event_handler(self, evt: MessageEvent) -> None:
    if evt.membership == 'join' and evt.prev_membership != 'join':
        for name, rule in self.config.rules.items():
            match = rule.match(evt)
            if match is not None:
            
