import click
import asyncio
from lib import api_request
from args import Argument


async def go(endpoint, path, method, other_opts):
    print(await api_request.call(endpoint, path, method, other_opts))




def main(endpoint, path, api_options, method):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    other_opts = parse_other_args(api_options)
    loop.run_until_complete(go(endpoint, path, method, other_opts))


if __name__ == "__main__":
    main()
