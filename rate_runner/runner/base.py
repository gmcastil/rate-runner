from abc import ABC, abstractmethod
from typing import Callable, Optional, Any

import requests

class BaseRunner(ABC):

    def __init__(self, session: requests.Session, user_config: dict,
                 on_status_update: Optional[Callable[dict, None]] = None):
        self.session = session
        self.user_config = user_config
        self.on_status_update = on_status_update
        self.cross_sections = []

    def configure(self, program) -> None:
        return

    def load(self, cross_sections: list[dict]) -> None:
        self.cross_sections = cross_sections
        return

    def run(self) -> None:
        return

