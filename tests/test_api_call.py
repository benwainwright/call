import unittest.mock
import pytest
import os

from call.api_requester import ApiRequester
from call.endpoint_manager import EndpointManager


@pytest.mark.asyncio
async def test_correct_api_call_is_made_when_passing_in_configured_alias(aresponses):
    mock_data = {
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
    }

    manager = EndpointManager(mock_data)

    aresponses.add(
        "jenkins.webcore.tools.bbc.co.uk",
        "/api/json",
        "get",
        aresponses.Response(
            text='{ "response" : "found" }',
            headers={"Content-Type": "application/json"},
        ),
    )
    requester = ApiRequester(manager)

    async with requester.do_call("jenkins", "list") as response:
        assert await response.json() == {"response": "found"}
