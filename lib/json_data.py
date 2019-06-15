import contextlib
import os
import json


def _make_file_dir_if_not_exists(path):
    dir = os.path.dirname(path)
    if not os.path.isdir(dir):
        os.makedirs(dir)


@contextlib.contextmanager
def data_from_json_file(path):
    _make_file_dir_if_not_exists(path)
    mode = "r+" if os.path.isfile(path) else "w+"
    with open(path, mode) as file:
        try:
            was_error = False
            try:
                json_data = json.load(file)
            except ValueError:
                json_data = {}
                was_error = True
            old_data = dict(json_data)
            yield json_data
        finally:
            if json_data != old_data or was_error:
                file.seek(0)
                file.truncate()
                file.write(json.dumps(json_data, indent=4))
