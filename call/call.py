import os

from call.template_loader import TemplateLoader
from call.pretty_json import pretty_json
from call.api_requester import ApiRequester

from jinja2 import TemplateError, Environment


class Call:
    def __init__(self, jinja_env: Environment, requester: ApiRequester):
        self.requester = requester
        self.jinja_env = jinja_env

    async def call_and_render(self, alias, path, args=None):
        async with self.requester.do_call(alias, path, args) as response:
            try:
                if response.status != 200:
                    template = self.jinja_env.get_template(
                        os.path.join(alias, "error.template")
                    )
                else:
                    template = self.jinja_env.get_template(
                        os.path.join(alias, f"{path}.template")
                    )
                return template.render(response=await response.json())
            except (OSError, TemplateError, AttributeError):
                return await response.text()
