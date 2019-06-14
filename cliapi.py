import aiohttp
import contextlib
import ssl
import urllib
import os
import urllib.parse
from jinja2 import Template

templates_dir = os.path.join(os.environ["HOME"], ".api-response-templates")


@contextlib.asynccontextmanager
async def get_session():
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


def get_template(method, url):
    parts = urllib.parse.urlparse(url)
    host_dir = os.path.join(templates_dir, parts.hostname)
    template_file = os.path.join(
        host_dir, method, parts.path.strip("/").replace("/", ":")
    )
    default_file = os.path.join(host_dir, "default")
    if os.path.isfile(template_file):
        with open(template_file) as file:
            return Template(file.read())
    elif os.path.isfile(default_file):
        with open(default_file) as file:
            return Template(file.read())


async def api_request(api_url, method="get", template_variant=None, values=None):
    async with get_session() as session:
        url = api_url.format(*values) if values else api_url
        async with session.get(url) as response:
            template = get_template("get", api_url)
            return (
                template.render(response=await response.json())
                if template
                else await response.text()
            )
