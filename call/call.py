import os

from call.template_loader import TemplateLoader
from call.pretty_json import pretty_json
from call.api_requester import ApiRequester

from jinja2 import Environment, TemplateError


class Call:
    def __init__(self, api_dir: str, requester: ApiRequester):
        self.api_dir = api_dir
        self.templates_dir = os.path.join(self.api_dir, "templates")
        self.jinja_env = Environment(loader=TemplateLoader(self.api_dir))
        self.jinja_env.filters["pretty_json"] = pretty_json
        self.requester = requester

    async def call_and_render(self, alias, path, method, args):
        async with self.requester.do_call(alias, path, method, args) as response:
            try:
                if response.status != 200:
                    template = self.jinja_env.get_template(
                        os.path.join(alias, "error.template")
                    )
                else:
                    template = jinja_env.get_template(
                        os.path.join(alias, method, f"{path}.template")
                    )
                return template.render(response=await response.json())
            except (OSError, TemplateError, AttributeError):
                return await response.text()
