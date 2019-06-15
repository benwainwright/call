import aiohttp
import contextlib
import ssl
import urllib
import os
import urllib.parse
from jinja2 import Template, TemplateError
from json_data import data_from_json_file

from endpoint import Endpoint

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
    with open(template_file, mode) as file:
        if mode == "w+":
            file.write("{{response}}")
        return Template(file.read())


def _get_path(data, alias, path):
    if "paths" not in data[alias]:
        data[alias]["paths"] = {}
    if path not in data[alias]["paths"]:
        path = _create_format_string_from_path(path)
        name = input(f"Enter path name for {alias}: {path}")
        data[alias]["paths"][name] = path
    return data[alias]["paths"][path]


def _make_url(alias_or_url, path, values):
    alias_file = os.path.join(cli_api_dir, "aliases.json")
    with data_from_json_file(alias_file) as data:
        endpoint = _create_true_endpoint(data, alias_or_url, path)
        return endpoint.get_url(values)


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


def _create_true_endpoint(data, endpoint, path=None):
    if endpoint not in data:
        parts = urllib.parse.urlparse(endpoint)
        endpoint = input(f"Enter alias for {parts.hostname}: ")
        data[endpoint] = {}
        data[endpoint]["base_url"] = f"{parts.scheme}://{parts.hostname}"
    if "paths" not in data[endpoint]:
        data[endpoint]["paths"] = {}
    if not path or path not in data[endpoint]["paths"]:
        path = path if path else parts.path
        path_string = _create_format_string_from_path(path)
        path = input(f"Enter path name for {endpoint} -> '{path}': ")
        data[endpoint]["paths"][path] = path_string
    return Endpoint(
        base_url=data[endpoint]["base_url"], path=data[endpoint]["paths"][path]
    )


async def api_request(alias, path, method="get", values=None, variant=None):
    async with _get_session() as session:
        url = _make_url(alias, path, values)
        async with session.get(url) as response:
            try:
                if response.status != 200:
                    template = _load_template_file_and_create_if_not_found(
                        templates_dir, alias, "error.template"
                    )
                else:
                    template = _load_template_file_and_create_if_not_found(
                        templates_dir, alias, method, f"{path}.template"
                    )
                return template.render(response=await response.json())
            except (OSError, TemplateError, AttributeError):
                return await response.text()

