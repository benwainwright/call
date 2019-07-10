import ssl
import aiohttp
import contextlib
import pyargs

from call.endpoint import Endpoint
from call.json_data_manager import JsonDataManager


class ApiRequester:
    def __init__(self, data_manager: JsonDataManager):
        self.data_manager = data_manager

    @contextlib.asynccontextmanager
    async def do_call(
        self, alias: str, path: str, parsed_arguments: [pyargs.Argument] = None
    ) -> aiohttp.ClientRequest:
        async with ApiRequester._get_session() as session:
            with self.data_manager.data() as data:
                if alias in data:
                    endpoint = Endpoint.from_dict(data[alias])
                    request = endpoint.build_request(path, parsed_arguments)
                    async with request.send(session) as response:
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
