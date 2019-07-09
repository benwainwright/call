import contextlib
import os
import json
import copy

from call.helpers import make_file_dir_if_not_exists


@contextlib.contextmanager
def data_from_json_file(path):
    make_file_dir_if_not_exists(path)
    mode = "r+" if os.path.isfile(path) else "w+"
    with open(path, mode) as file:
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
