import pyargs
import urllib.parse

from dataclasses import dataclass

from call.endpoint.path import Path
from call.request import Request
from call.endpoint.option import Option


@dataclass
class Endpoint:

    name: str
    base_url: str
    paths: {str: Path} = None

    def build_request(
        self, path_name: str, arguments: pyargs.ParsedArguments = None
    ) -> Request:

        if path_name in self.paths:
            path = self.paths[path_name]
            url = urllib.parse.urljoin(self.base_url, path.route)
            if arguments is None:
                return Request(url=url, method=path.method)

            parts = urllib.parse.urlparse(url)
            query_pairs = [
                pair.split("=", 1) for pair in parts.query.split("&") if len(pair) > 0
            ]
            names = [option.name for option in path.options]
            values = [
                arg.value for name in names for arg in arguments if arg.name == name
            ]

        return Request(url=url.format(*values), method=path.method)

    @staticmethod
    def from_dict(data: {}):
        print(data)
        return Endpoint(
            name=data["name"],
            base_url=data["base_url"],
            paths={
                alias: Path(
                    method=method,
                    name=alias,
                    description=data["paths"][method][alias]["description"],
                    route=data["paths"][method][alias]["route"],
                    options=[
                        Option(name=option["name"], description=option["description"])
                        for option in data["paths"][method][alias]["options"]
                    ],
                )
                for method in data["paths"]
                for alias in data["paths"][method]
            },
        )

    def to_dict(self):
        print(self)
        return {
            "name": self.name,
            "base_url": self.base_url,
            "paths": {
                method: {
                    path.name: {
                        "route": path.route,
                        "description": path.description,
                        "options": [
                            {"name": option.name, "description": option.description}
                            for option in path.options
                        ],
                    }
                    for path in self.paths.values()
                    if path.method == method
                }
                for method in {path.method for path in self.paths.values()}
            },
        }