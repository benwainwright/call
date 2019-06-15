import aiohttp
import contextlib
import ssl
import urllib
import os
import urllib.parse
from jinja2 import Environment, TemplateError

from lib.json_data import data_from_json_file
from lib.endpoint import Endpoint
from lib.template_loader import TemplateLoader
from lib.pretty_json import pretty_json


cli_api_dir = os.path.join(os.environ["HOME"], ".call")
templates_dir = os.path.join(cli_api_dir, "templates")
jinja_env = Environment(loader=TemplateLoader(cli_api_dir))

jinja_env.filters["pretty_json"] = pretty_json


@contextlib.asynccontextmanager
async def _get_session():
    try:
        sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
        sslcontext.load_cert_chain(
            certfile="/etc/pki/tls/certs/client.crt",
            keyfile="/etc/pki/tls/private/client.key",
        )
        connector = aiohttp.TCPConnector(ssl=sslcontext)
        session = aiohttp.ClientSession(trust_env=True, connector=connector)
        yield session
    finally:
        await session.close()


def _get_endpoint_from_alias_file(endpoint, path, method):
    alias_file = os.path.join(cli_api_dir, "aliases.json")
    with data_from_json_file(alias_file) as data:
        return _build_endpoint(data, endpoint, path, method)


def _create_format_string_from_url(path, query):
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
    indexes = [int(num.strip()) for num in placeholders.strip().split(",")]

    for index in (i for i in indexes if i < len(segments)):
        segments[index] = "{}"

    print(len(query))
    if len(query_parts) > 0:
        for index in (i - len(segments) for i in indexes if i >= len(segments)):
            pair = query_parts[index].split("=", 1)
            pair[1] = "{}"
            query_parts[index] = "=".join(pair)

    return "/".join(segments), "&".join(query_parts)


def _make_path(data, endpoint, path, query, method):
    if "paths" not in data[endpoint]:
        data[endpoint]["paths"] = {}
    if method not in data[endpoint]["paths"]:
        data[endpoint]["paths"][method] = {}
    if not path or path not in data[endpoint]["paths"][method]:
        path_string, query_string = _create_format_string_from_url(path, query)
        full_string = (
            f"{path_string}?{query_string}" if len(query_string) > 0 else path_string
        )
        path = input(f"Enter path name for {endpoint} -> '{full_string}': ")
        data[endpoint]["paths"][method][path] = {}
        data[endpoint]["paths"][method][path][
            "string"
        ] = full_string
        option_count = len(path_string.split("{}")) - 1
        data[endpoint]["paths"][method][path]["path_options"] = []
        if (option_count) > 0:
            print(f"Enter variable names for {path_string}")

        for i in range(option_count):
            name = input(f"{i}: ")
            data[endpoint]["paths"][method][path]["path_options"].append(name)

        for pair in query_string.split("&"):
            pair = pair.split("=", 1)
            if len(pair) > 1 and pair[1] == "{}":
                data[endpoint]["paths"][method][path]["path_options"].append(pair[0])
    return path


def _build_endpoint(data, endpoint, path, method):
    parts = urllib.parse.urlparse(endpoint)
    if endpoint not in data:
        base_url = f"{parts.scheme}://{parts.hostname}"
        found = [key for key in data.keys() if data[key]["base_url"] == base_url]
        if len(found) > 0:
            endpoint = found[0]
            print(f"'{base_url}' is already aliased to '{endpoint}'")
        else:
            endpoint = input(f"Enter alias for {base_url}: ")
            data[endpoint] = {}
            data[endpoint]["base_url"] = base_url
    path = _make_path(data, endpoint, path if path else parts.path, parts.query, method)
    return Endpoint(
        method=method,
        name=endpoint,
        base_url=data[endpoint]["base_url"],
        path_string=data[endpoint]["paths"][method][path]["string"],
        path_name=path,
        option_names=data[endpoint]["paths"][method][path]["path_options"],
    )


def get_response_template(response, endpoint):
    if response.status != 200:
        return jinja_env.get_template(os.path.join(endpoint.name, "error.template"))
    else:
        return jinja_env.get_template(
            os.path.join(
                endpoint.name, endpoint.method, f"{endpoint.path_name}.template"
            )
        )


async def call(endpoint, path, method="get", other_opts=None):
    async with _get_session() as session:
        endpoint = _get_endpoint_from_alias_file(endpoint, path, method)
        url = endpoint.get_url(other_opts)
        async with session.get(url) as response:
            try:
                template = get_response_template(response, endpoint)
                return template.render(response=await response.json())
            except (OSError, TemplateError, AttributeError):
                return await response.text()
