import json
from pygments import highlight, lexers, formatters


def pretty_json(data):
    json_string = json.dumps(data, sort_keys=True, indent=4)
    return highlight(
        json_string,
        lexers.JsonLexer(),
        formatters.TerminalFormatter(),
    )
