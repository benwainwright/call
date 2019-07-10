import click
import asyncio

import call.config
from call import ApiRequester, JsonDataManager, Call, pretty_json, TemplateLoader
from jinja2 import Environment, TemplateError

async def go(endpoint, path, method, other_opts):

    jinja_env = Environment(loader=TemplateLoader(call.config.CLI_API_DIR))
    jinja_env.filters["pretty_json"] = pretty_json
    data_manager = JsonDataManager(call.config.ALIAS_FILE)
    requester = ApiRequester(data_manager)
    caller = Call(jinja_env, requester)


def main(endpoint, path, api_options, method):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    other_opts = parse_other_args(api_options)
    loop.run_until_complete(go(endpoint, path, method, other_opts))


if __name__ == "__main__":
    main()
