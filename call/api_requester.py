import ssl
import aiohttp
import contextlib
import pyargs

from call.endpoint import Endpoint


class ApiRequester:

    def __init__(self, data_manager, alias_file):
        self.data_manager = data_manager
        self.alias_file = alias_file

    @contextlib.asynccontextmanager
    async def do_call(
        self, alias, path, method="get", parsed_arguments: [pyargs.Argument] = None
    ) -> aiohttp.ClientRequest:
        async with ApiRequester._get_session() as session:
            with self.data_manager(self.alias_file) as data:
                endpoint = Endpoint.from_data(data, alias, path, method)
                url = endpoint.get_url(parsed_arguments)
                async with session.request(method, url) as response:
                    yield response

    @staticmethod
    @contextlib.asynccontextmanager
    async def _get_session() -> aiohttp.ClientSession:
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
