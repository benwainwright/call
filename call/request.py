import contextlib

import aiohttp

from dataclasses import dataclass


@dataclass
class Request:

    method: str
    url: str

    def send(self, session: aiohttp.ClientSession):
        return session.request(self.method, self.url)
