import contextlib
import os
import json
import copy


class JsonDataManager:
    def __init__(self, path: str):
        dir = os.path.dirname(path)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        self.path = path

    @contextlib.contextmanager
    def data(self):
        mode = "r+" if os.path.isfile(self.path) else "w+"
        with open(self.path, mode) as file:
            try:
                was_error = False
                try:
                    json_data = json.load(file)
                except ValueError:
                    json_data = {}
                    was_error = True
                old_data = copy.deepcopy(json_data)
                yield json_data
            finally:
                if json_data != old_data or was_error:
                    file.seek(0)
                    file.truncate()
                    file.write(json.dumps(json_data, indent=4))
