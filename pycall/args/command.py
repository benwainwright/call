import sys
from typing import Callable

from dataclasses import dataclass
from pycall.args.argument_schema import ArgumentSchema
from pycall.args.errors.missing_required_arguments_error import MissingRequiredArgumentsError
from pycall.args.errors.bad_usage_error import BadUsageError
from pycall.args.parsed_arguments import ParsedArguments


@dataclass
class Command:
    def __init__(
        self,
        name: str,
        function: Callable = None,
        schema: ArgumentSchema = None,
        description: str = None,
        subcommands: ["Command"] = None,
        parent: "Command" = None,
    ):
        if function is None and subcommands is None:
            raise ValueError(
                "Command initialised without subcommands must have a function"
            )
        self.name = name
        self.description = description
        self.subcommands = (
            {command.name: command for command in subcommands} if subcommands else {}
        )
        self.function = function
        self.schema = schema
        self.parent = None
        for subcommand in self.subcommands.values():
            subcommand.parent = self

    def command_path(self):
        if self.parent == None:
            return sys.argv[0]

        return f"{self.parent.command_path()} {self.name}"

    def usage_string(self):
        if len(self.subcommands.keys()) > 0:
            usage = f"{self.command_path()} [SUBCOMMAND]"
        elif self.schema is not None:
            usage = f"{self.command_path()}"
            usage = (
                f"{usage} {self.schema.arg_usage()}"
                if self.schema is not None
                else usage
            )
        else:
            usage = f"{self.command_path()}"
        return usage

    def describe_options(self):
        if len(self.subcommands.keys()) > 0:
            return [
                f"{command.name}\t{command.description}"
                for command in self.subcommands.values()
            ]
        elif self.schema is not None:
            return self.schema.describe_args()
        else:
            return []

    def execute_or_print_usage(self, args: [str]):
        try:
            self.execute(args)
        except BadUsageError as ex:
            print(f"Error! {ex.message}\n")
            print(f"Usage: {ex.usage}")
            print(
                f'\n(arguments can also be supplied in "named" form: e.g. --<NAME> <VALUE>)\n'
            )
            print(f"Details:")
            print("\n".join(ex.options))

    def execute(self, args: [str]):
        if self.parent is None:
            args = args[1:]

        positional, named = Command.parse_args(args)

        if len(self.subcommands.keys()) > 0:
            if len(positional) > 0 and positional[0] in self.subcommands.keys():
                args.remove(positional[0])
                self.subcommands[positional[0]].execute(args)
            else:
                raise BadUsageError(
                    "Missing subcommand", self.usage_string(), self.describe_options()
                )
        else:
            try:
                if self.schema is not None:
                    (args, unknown_named, unknown_positional) = self.schema.hydrate(
                        positional, named
                    )
                    result = (self, args, unknown_named, unknown_positional)
                else:
                    result = (positional, named)
                self.function(*result)
            except MissingRequiredArgumentsError as ex:
                raise BadUsageError(
                    str(ex), self.usage_string(), self.describe_options()
                )

    @staticmethod
    def parse_args(args: []) -> ([], {}):
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
        return positional, named
