import sys

from pyargs import Command, Argument, ArgumentSchema, BadUsageError

from call.add_endpoint import add_endpoint_command

schema = ArgumentSchema(
    args=[
        Argument(
            name="url",
            short="u",
            description="The full url of the endpoint you want to alias",
            required=True,
        ),
        Argument(
            name="alias",
            short="a",
            description="The name you wish to use to refer to this url",
            required=False,
        ),
    ]
)


add_endpoint_command = Command(
    "Add endpoint", function=add_endpoint_command, schema=schema
)

add_endpoint_command.execute_or_print_usage(sys.argv)
