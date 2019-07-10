import pyargs
import urllib.parse

from dataclasses import dataclass

from call.path import Path
from call.request import Request


@dataclass
class Endpoint:

    name: str
    base_url: str
    paths: {str: Path} = None

    def build_request(
        self, path_name: str, arguments: [pyargs.Argument] = None
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
            names = self.option_names + [
                pair[0] for pair in query_pairs if len(pair) > 1 and pair[1] == "{}"
            ]
            values = [
                arg.value for name in names for arg in arguments if arg.name == name
            ]

        return Request(url=url.format(*values), method=path.method)

    @staticmethod
    def from_dict(data: {}):
        return Endpoint(
            name=data["name"],
            base_url=data["base_url"],
            paths={
                alias: Path(
                    method=method,
                    name=alias,
                    route=data["paths"][method][alias]["route"],
                    options=data["paths"][method][alias]["options"],
                )
                for method in data["paths"]
                for alias in data["paths"][method]
            },
        )

    def to_dict(self):
        return {
            "name": self.name,
            "base_url": self.base_url,
            "paths": {
                method: {
                    path.name: {"route": path.route, "options": path.options}
                    for path in self.paths
                    if path.method == method
                }
                for method in {path.method for path in self.paths}
            },
        }

    # @staticmethod
    # def from_data(data, alias, path, method):
    #     options = None
    #     if alias in data:
    #         if method in data[alias]["paths"]:
    #             if path in data[alias]["paths"][method]:
    #                 path_string = data[alias]["paths"][method][path]["string"]
    #             else:
    #                 path_string = path

    #                 options = (
    #                     data[alias]["paths"][method][path]["path_options"]
    #                     if "path_options" in data[alias]["paths"][method][path]
    #                     else None
    #                 )

    #         return Endpoint(
    #             name=alias,
    #             base_url=data[alias]["base_url"],
    #             path_string=path_string,
    #             path_name=path,
    #             method=method,
    #             option_names=options,
    #         )

    # @staticmethod
    # def build(data, url):
    #     parts = urllib.parse.urlparse(url)
    #     base_url = f"{parts.scheme}://{parts.hostname}"
    #     found = [key for key in data.keys() if data[key]["base_url"] == base_url]
    #     if len(found) > 0:
    #         endpoint = found[0]
    #         print(f"'{base_url}' is already aliased to '{endpoint}'")
    #     else:
    #         endpoint = input(f"Enter alias for {base_url}: ")
    #         data[endpoint] = {}
    #         data[endpoint]["base_url"] = base_url
    #     return Endpoint(name=data)
