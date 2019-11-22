class BadUsageError(ValueError):

    def __init__(self, message: str, usage: str, options: str):
        self.message = message
        self.usage = usage
        self.options = options
