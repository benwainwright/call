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


async def call_api(alias, path, args):
    jinja_env = Environment(loader=TemplateLoader(call.config.CLI_API_DIR))
    jinja_env.filters["pretty_json"] = pretty_json
    data_manager = JsonDataManager(call.config.ALIAS_FILE)
    with data_manager.data() as data:
        endpoints = EndpointManager(data)
        requester = ApiRequester(endpoints)
        caller = Call(jinja_env, requester)
        print(await caller.call_and_render(alias, path, args.values()))


def go(arguments):
    alias = arguments.command.parent.name
    path = arguments.command.name
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(call_api(alias, path, arguments.args))


data_manager = JsonDataManager(call.config.ALIAS_FILE)
with data_manager.data() as data:
    endpoints = EndpointManager(data)
    call_command = Command(
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
    call_command.execute(sys.argv)
except BadUsageError as ex:
    print(f"Error! {ex.message}\n")
    print(f"Usage: {ex.usage}")
    print(f"\nPossible arguments (can be either POSITIONAL or NAMED arguments):\n")
    print("\n".join(ex.options))
