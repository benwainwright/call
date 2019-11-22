from dataclasses import dataclass


@dataclass
class ParsedArguments:

    args: {}

    def __getattr__(self, name):
        if name in self.args:
            return self.args[name].value

    def __iter__(self):
        return self.args.values().__iter__()
