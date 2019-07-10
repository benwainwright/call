import asyncio
from pyargs import Command, Argument, ArgumentSchema, BadUsageError

import click
import sys
from jinja2 import Environment, TemplateError

import call.config
from call import (
    ApiRequester,
    Call,
    EndpointManager,
    JsonDataManager,
    TemplateLoader,
    pretty_json,
)
from call.endpoint_manager import EndpointManager


async def go(endpoint, path, method, other_opts):
    jinja_env = Environment(loader=TemplateLoader(call.config.CLI_API_DIR))
    jinja_env.filters["pretty_json"] = pretty_json
    data_manager = JsonDataManager(call.config.ALIAS_FILE)
    with data_manager.data() as data:
        endpoints = EndpointManager(data)
        requester = ApiRequester(endpoints)
        caller = Call(jinja_env, requester)


# def main(endpoint, path, api_options, method):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     other_opts = parse_other_args(api_options)
#     loop.run_until_complete(go(endpoint, path, method, other_opts))


def go(arguments):
    pass


data_manager = JsonDataManager(call.config.ALIAS_FILE)
with data_manager.data() as data:
    endpoints = EndpointManager(data)
    call = Command(
        name="call",
        subcommands=[
            Command(
                name=endpoint.name,
                description=endpoint.base_url,
                subcommands=[
                    Command(
                        name=path.name,
                        description=f"{endpoint.name} -> {path.method.upper()} -> {path.route}",
                        function=go,
                        schema=ArgumentSchema(
                            args=[
                                Argument(name=option, description="foo")
                                for option in path.options
                            ]
                        ),
                    )
                    for path in endpoint.paths.values()
                ],
            )
            for endpoint in endpoints
        ],
    )

try:
    call.execute(sys.argv)
except BadUsageError as ex:
    print(f"Error! {ex.message}\n")
    print(f"Usage: {ex.usage}")
    print(f"\nPossible arguments (can be either POSITIONAL or NAMED arguments):\n")
    print("\n".join(ex.options))
