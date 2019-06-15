import urllib.parse
from dataclasses import dataclass


@dataclass
class Endpoint:

    name: str
    base_url: str
    path_string: str
    path_name: str
    method: str

    def get_url(self, values: [str] = None):
        url = urllib.parse.urljoin(self.base_url, self.path_string)
        return url.format(*values) if values else url
