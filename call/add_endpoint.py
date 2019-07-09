import urllib
import call.endpoint
import call.path
import call.config
import call.json_data
from builtins import ValueError


def add_endpoint_command(arguments):
    if "url" not in arguments.args:
        raise ValueError("Url not supplied")

    _add_endpoint_alias(
        arguments.args["url"],
        arguments.args["alias"] if "alias" in arguments.args else None,
    )


def _add_endpoint_alias(url, alias=None, route_name=None, method="get"):
    with call.json_data.data_from_json_file(call.config.ALIAS_FILE) as data:
        parts = urllib.parse.urlparse(url)
        base_url = f"{parts.scheme}://{parts.hostname}"

        alias = _get_alias_name(base_url, data)

        if alias in data:
            endpoint = call.Endpoint.from_dict(data[alias])
        else:
            endpoint = call.endpoint.Endpoint(name=alias, base_url=base_url, paths=[])

        endpoint.paths.append(
            _make_new_path_alias(
                alias, base_url, parts.path, parts.query, method, route_name
            )
        )

        data[alias] = endpoint.to_dict()


def _create_format_string_from_url(path, query) -> str:
    print("Pleae identify variable url segments: ")
    print(f"\nPath '{path}'")
    segments = path.strip("/").split("/")
    placeholders = [f"{i}: {segment}" for i, segment in enumerate(segments)]
    print("\n".join(placeholders))
    if len(query) > 0:
        query_parts = query.split("&")
        print(f"\nQuery string '{query}'")
        query_placeholders = [
            f"{i + len(segments)}: {segment}" for i, segment in enumerate(query_parts)
        ]
        print("\n".join(query_placeholders))
    else:
        query_parts = []

    placeholders = input("\nEnter comma separated list of numbers: ")
    indexes = [int(num.strip()) for num in placeholders.strip().split(",")] if len(placeholders) > 0 else []
    for index in (i for i in indexes if i < len(segments)):
        segments[index] = "{}"

    print(len(query))
    if len(query_parts) > 0:
        for index in (i - len(segments) for i in indexes if i >= len(segments)):
            pair = query_parts[index].split("=", 1)
            pair[1] = "{}"
            query_parts[index] = "=".join(pair)

    return "/".join(segments), "&".join(query_parts)


def _get_option_names(path_string, query_string):
    options = []
    option_count = len(path_string.split("{}")) - 1
    if (option_count) > 0:
        print(f"Enter variable names for {path_string}")

        for i in range(option_count):
            name = input(f"{i}: ")
            options.append(name)

        for pair in query_string.split("&"):
            pair = pair.split("=", 1)
            if len(pair) > 1 and pair[1] == "{}":
                options.append(pair[0])
    return options


def _get_alias_name(base_url, data):
    found_aliases = [
        alias["name"] for alias in data.values() if alias["base_url"] == base_url
    ]

    return (
        found_aliases[0]
        if len(found_aliases) > 0
        else input(f"Enter alias for {base_url}")
    )


def _make_new_path_alias(
    alias, base_url, path, query, method, route_name
) -> call.path.Path:
    name = (
        route_name
        if route_name is not None
        else input(f"Enter path name for {method.upper()} {alias} {path}: ")
    )

    path_string, query_string = _create_format_string_from_url(path, query)
    full_string = (
        f"{path_string}?{query_string}" if len(query_string) > 0 else path_string
    )

    return call.path.Path(
        method=method,
        name=name,
        route=full_string,
        options=_get_option_names(path_string, query_string),
    )

