import aiohttp
import contextlib
import ssl
import urllib
import os
import urllib.parse
from jinja2 import Template, TemplateError

from lib.json_data import data_from_json_file
from lib.endpoint import Endpoint
from lib.helpers import make_file_dir_if_not_exists

cli_api_dir = os.path.join(os.environ["HOME"], ".cli-api")
templates_dir = os.path.join(cli_api_dir, "templates")


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


def _load_template_file_and_create_if_not_found(*paths):
    template_file = os.path.join(*paths)
    mode = "r+" if os.path.isfile(template_file) else "w+"
    make_file_dir_if_not_exists(template_file)
    with open(template_file, mode) as file:
        if mode == "w+":
            file.write("{{ response|pprint }}")
        return Template(file.read())


def _get_path(data, alias, path):
    if "paths" not in data[alias]:
        data[alias]["paths"] = {}
    if path not in data[alias]["paths"]:
        path = _create_format_string_from_path(path)
        name = input(f"Enter path name for {alias}: {path}")
        data[alias]["paths"][name] = path
    return data[alias]["paths"][path]


def _get_endpoint_from_alias_file(endpoint, path, method):
    alias_file = os.path.join(cli_api_dir, "aliases.json")
    with data_from_json_file(alias_file) as data:
        return _build_endpoint(data, endpoint, path, method)


def _create_format_string_from_path(path):
    print("Which path segments are variables?")
    segments = path.strip("/").split("/")
    placeholders = [f"{i}: {segment}" for i, segment in enumerate(segments)]
    print("\n".join(placeholders))
    placeholders = input("Enter comma separated list of numbers: ")
    indexes = [int(num.strip()) for num in placeholders]
    for index in indexes:
        segments[index] = "{}"
    return "/".join(segments)


def _build_endpoint(data, endpoint, path, method):
    if endpoint not in data:
        parts = urllib.parse.urlparse(endpoint)
        endpoint = input(f"Enter alias for {parts.hostname}: ")
        data[endpoint] = {}
        data[endpoint]["base_url"] = f"{parts.scheme}://{parts.hostname}"
    if "paths" not in data[endpoint]:
        data[endpoint]["paths"] = {}
    if method not in data[endpoint]["paths"]:
        data[endpoint]["paths"][method] = {}
    if not path or path not in data[endpoint]["paths"][method]:
        path = path if path else parts.path
        path_string = _create_format_string_from_path(path)
        path = input(f"Enter path name for {endpoint} -> '{path}': ")
        data[endpoint]["paths"][method][path] = path_string
    return Endpoint(
        method=method,
        name=endpoint,
        base_url=data[endpoint]["base_url"],
        path_string=data[endpoint]["paths"][method][path],
        path_name=path,
    )


async def call(endpoint, path, method="get", values=None, variant=None):
    async with _get_session() as session:
        endpoint = _get_endpoint_from_alias_file(endpoint, path, method)
        async with session.get(endpoint.get_url(values)) as response:
            try:
                if response.status != 200:
                    template = _load_template_file_and_create_if_not_found(
                        templates_dir, endpoint.name, "error.template"
                    )
                else:
                    template = _load_template_file_and_create_if_not_found(
                        templates_dir,
                        endpoint.name,
                        endpoint.method,
                        f"{endpoint.path_name}.template",
                    )
                return template.render(response=await response.json())
            except (OSError, TemplateError, AttributeError):
                return await response.text()
