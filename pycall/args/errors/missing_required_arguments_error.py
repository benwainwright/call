from pycall.args.argument import Argument


class MissingRequiredArgumentsError(ValueError):

    def __init__(self, args: [Argument]):
        self.args = args

    def __str__(self):
        argument_plural_or_not_string = "arguments" if len(
            self.args) > 1 else "argument"
        arg_names = ", ".join(arg.name for arg in self.args)
        return f"Missing the following required {argument_plural_or_not_string}: {arg_names}"
