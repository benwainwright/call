import unittest
import builtins
from call.add_endpoint import _add_endpoint_alias


def test_adding_endpoint_with_variables_results_in_correct_alias():

    i = 0

    def mock_input(prompt):
        if "alias" in prompt.lower():
            return "github"

        if "path name" in prompt.lower():
            return "repo"

        if "comma separated list of numbers" in prompt.lower():
            return "1,2"

        nonlocal i
        if i == 0:
            i += 1
            return "org"

        if i == 1:
            return "name"

    input_data = "https://api.github.com/repos/docker/docker.github.io/pulls"
    output_data = """\
{
    "github": {
        "name": "github",
        "base_url": "https://api.github.com",
        "paths": {
            "get": {
                "repo": {
                    "route": "repos/{}/{}/pulls",
                    "options": [
                        "org",
                        "name"
                    ]
                }
            }
        }
    }
}"""

    m = unittest.mock.mock_open()
    with unittest.mock.patch("builtins.input", mock_input):
        with unittest.mock.patch("builtins.open", m, create=True):
            _add_endpoint_alias(input_data)

    handle = m()
    handle.write.assert_called_once_with(output_data)


def test_adding_endpoint_without_any_options_results_in_simple_alias():
    def mock_input(prompt):
        if "alias" in prompt.lower():
            return "jenkins"

        if "variable names" in prompt.lower():
            return ""

        if "path name" in prompt.lower():
            return "list"

        if "comma separated list of numbers" in prompt.lower():
            return ""

    input_data = "https://jenkins.webcore.tools.bbc.co.uk/api/json"
    output_data = """\
{
    "jenkins": {
        "name": "jenkins",
        "base_url": "https://jenkins.webcore.tools.bbc.co.uk",
        "paths": {
            "get": {
                "list": {
                    "route": "api/json",
                    "options": []
                }
            }
        }
    }
}"""

    m = unittest.mock.mock_open()
    with unittest.mock.patch("builtins.input", mock_input):
        with unittest.mock.patch("builtins.open", m, create=True):
            _add_endpoint_alias(input_data)

    handle = m()
    handle.write.assert_called_once_with(output_data)
