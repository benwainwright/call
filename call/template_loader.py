import os
from jinja2 import BaseLoader
from call.helpers import make_file_dir_if_not_exists

default_template = "{{ response|pretty_json }}"


class TemplateLoader(BaseLoader):
    def __init__(self, call_dir):
        self.templates_dir = os.path.join(call_dir, "templates")

    def get_source(self, environment, template):
        template_file = os.path.join(self.templates_dir, template)
        mode = "r+" if os.path.isfile(template_file) else "w+"
        make_file_dir_if_not_exists(template_file)
        with open(template_file, mode) as file:
            if mode == "w+":
                file.write(default_template)
            mtime = os.path.getmtime(template_file)
            return (
                file.read(),
                template_file,
                lambda: mtime == os.path.getmtime(template_file),
            )
