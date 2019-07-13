import asyncio
from pyargs import Command, Argument, ArgumentSchema, BadUsageError

import sys
from jinja2 import Environment

import call.config
from call import (
    ApiRequester,
    Call,
    EndpointManager,
    JsonDataManager,
    TemplateLoader,
    pretty_json,
)


async def call_api(alias, path, args):
    jinja_env = Environment(loader=TemplateLoader(call.config.CLI_API_DIR))
    jinja_env.filters["pretty_json"] = pretty_json
    data_manager = JsonDataManager(call.config.ALIAS_FILE)
    with data_manager.data() as data:
        endpoints = EndpointManager(data)
        requester = ApiRequester(endpoints)
        caller = Call(jinja_env, requester)
        print(await caller.call_and_render(alias, path, args))


def go(command, args, unknown_named, unknown_positional):
    alias = command.parent.name
    path = command.name
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(call_api(alias, path, args))


def configure_command_from_endpoint_data(endpoint):
    return Command(
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


data_manager = JsonDataManager(call.config.ALIAS_FILE)
with data_manager.data() as data:
    endpoints = EndpointManager(data)
    if len(endpoints) > 0:
        command = configure_command_from_endpoint_data(endpoints)
        command.execute_or_print_usage(sys.argv)
    else:
        print(
            "No endpoints configured. You can use the accompanying 'add-endpoint' utility to do this"
        )
