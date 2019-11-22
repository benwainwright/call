import collections
from collections import OrderedDict

from pycall.args.argument import Argument
from pycall.args.errors.missing_required_arguments_error import MissingRequiredArgumentsError
from pycall.args.parsed_arguments import ParsedArguments


class ArgumentSchema:
    def __init__(self, args=[Argument]):
        self.args = collections.OrderedDict((arg.name, arg) for arg in args)
        self.positional = []
        self.named = {}

    def __getattr__(self, name: str):
        if name in self.named:
            return self.named[name]

        positional_dict = {arg.name: arg for arg in self.positional}

        if name in positional_dict:
            return positional_dict[name]

    def __len__(self):
        return len(self.positional)

    def __getitem__(self, key) -> str:
        if key < len(self.positional):
            return self.positional[key]

    def _values_as_dict(self):
        positional_dict = {arg.name: arg for arg in self.positional}
        combined = {**self.named, **positional_dict}
        return {arg.name: arg.value for arg in combined.values()}

    def arg_usage(self):
         required = " ".join(f"<{arg.name.upper()}>" for arg in self.args.values() if arg.required == True)
         optional = " ".join(f"<{arg.name.upper()}>" for arg in self.args.values() if arg.required == False)
         return f"{required} [{optional}]" if len(optional) > 0 else required

    def describe_args(self):
        return [f"{arg.name}\t\t{arg.description}" for arg in self.args.values()]

    def description_string(self):
        positional_lines = [arg.description_string(False) for arg in self.positional]
        named_lines = [arg.description_string(True) for arg in self.named.values()]
        lines = positional_lines + named_lines
        return "\n".join(lines)

    def hydrate(self, positional, named):
        args = list(self.args.values())
        missing_required = []
        i = 0
        for i, arg in enumerate(args):
            if i < len(positional):
                arg.value = positional[i]
                self.positional.append(arg)
            elif arg.name in named:
                arg.value = named[args[i].name]
                self.named[arg.name] = arg
            elif arg.required:
                missing_required.append(arg)

        if len(missing_required) > 0:
            raise MissingRequiredArgumentsError(missing_required)

        unknown_positional = (
            positional[len(self.positional) :]
            if len(self.positional) < len(positional)
            else []
        )

        unknown_named = {
            key: value for (key, value) in named.items() if key not in self.named.keys()
        }

        return ParsedArguments(args=self.args), unknown_named, unknown_positional
