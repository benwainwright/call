from dataclasses import dataclass


@dataclass
class Path:

    method: str
    name: str
    route: str
    options: [str]
