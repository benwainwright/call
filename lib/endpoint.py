import urllib.parse
from dataclasses import dataclass


@dataclass
class Endpoint:

    base_url: str
    path: str

    def get_url(self, values: [str] = None):
        url = urllib.parse.urljoin(self.base_url, self.path)
        return url.format(*values) if values else url
