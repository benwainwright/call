import click
import asyncio
from lib import api_request


async def go(endpoint, path, method, value):
    print(await api_request.call(endpoint, path, method, value))


@click.command()
@click.argument("endpoint")
@click.argument("path", required=False)
@click.option("--method", default="get")
@click.option("--value", multiple=True)
def main(endpoint, path, method, value):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(go(endpoint, path, method, value))


if __name__ == "__main__":
    main()
