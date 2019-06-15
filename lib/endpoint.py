import urllib.parse
from dataclasses import dataclass


@dataclass
class Endpoint:

    name: str
    base_url: str
    path_string: str
    path_name: str
    method: str
    option_names: []

    def get_url(self, options_provided=None):
        url = urllib.parse.urljoin(self.base_url, self.path_string)

        positional = options_provided["positional"]
        named = options_provided["named"]

        from_positional_args = [
            {"name": self.option_names[i], "value": arg}
            for i, arg in enumerate(positional)
            if i < len(self.option_names)
        ]

        found_so_far = [item["name"] for item in from_positional_args]

        from_option_args = [
            {"name": key, "value": named[key]}
            for key in self.option_names
            if key not in found_so_far and key in named
        ]

        all_found = from_positional_args + from_option_args

        missing = len(self.option_names) - len(all_found)

        if missing > 0:
            missing = [self.option_names[i] for i in range(missing)]
            raise ValueError("Missing arguments " + str(missing))

        values = [item["value"] for item in all_found]

        return url.format(*values)
