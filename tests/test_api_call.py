import unittest.mock
import pytest
import os

from call.api_requester import ApiRequester
from call.json_data import data_from_json_file


@pytest.mark.asyncio
async def test_correct_api_call_is_made_when_passing_in_configured_alias(aresponses):
    mock_data = """{
        "jenkins": {
            "base_url": "https://jenkins.webcore.tools.bbc.co.uk",
            "paths": {
                "get": {
                    "list": {
                        "string": "api/json"
                    }
                }
            }
        }
    }
    """
    mocked_open = unittest.mock.mock_open(read_data=mock_data)

    aresponses.add(
        "jenkins.webcore.tools.bbc.co.uk",
        "/api/json",
        "get",
        aresponses.Response(
            text='{ "response" : "found" }',
            headers={"Content-Type": "application/json"},
        ),
    )
    with unittest.mock.patch("call.json_data.open", mocked_open):
        requester = ApiRequester(
            data_from_json_file, os.path.join(os.getcwd(), "tests", "aliases.json")
        )

        async with requester.do_call("jenkins", "list") as response:
            assert await response.json() == {"response": "found"}
