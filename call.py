import click
import asyncio
from lib import api_request


async def go(endpoint, path, method, other_opts):
    print(await api_request.call(endpoint, path, method, other_opts))


def parse_other_args(args):
    named = {
        value: args[i + 1]
        for i, value in enumerate(args)
        if value.startswith("--") and i + 1 < len(args)
    }
    positional = [
        item
        for item in args
        if item not in set(list(named.keys()) + list(named.values()))
    ]
    named = {key[2:]: named[key] for key in named}
    return {"named": named, "positional": positional}


@click.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)
@click.argument("endpoint")
@click.argument("path", required=False)
@click.argument("api_options", nargs=-1)
@click.option("--method", default="get")
def main(endpoint, path, api_options, method):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    other_opts = parse_other_args(api_options)
    loop.run_until_complete(go(endpoint, path, method, other_opts))


if __name__ == "__main__":
    main()
