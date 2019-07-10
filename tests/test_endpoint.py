import pyargs

from call.endpoint import Endpoint
from call.path import Path


def test_correctly_constructs_url_without_options():

    endpoint = Endpoint(
        name="foo",
        base_url="https://www.google.com",
        paths= {
            "foo": Path(
                method="get",
                name="foo",
                route="foo/bar",
                options=[]
            )
        }
    )

    request = endpoint.build_request("foo")

    assert request.url == "https://www.google.com/foo/bar"
    assert request.method == "get"


def test_correctly_constructs_url_with_single_arg():

    endpoint = Endpoint(
        name="foo",
        base_url="https://www.google.com",
        paths={
            "foo": Path(
                method="get",
                name="foo",
                route="foo/bar/{}/bar",
                options=["foo"]
            )
        }
    )

    args = [
        pyargs.Argument(
            name="foo",
            description="blah",
            required=True,
            value="baz"
        )
    ]

    request = endpoint.build_request("foo", args)

    assert request.url == "https://www.google.com/foo/bar/baz/bar"
    assert request.method == "get"

def test_correctly_constructs_url_with_query_that_has_constant_parts():
    endpoint = Endpoint(
        name="foo",
        base_url="https://www.google.com",
        paths={
            "foo": Path(
                method="get",
                name="foo",
                route="foo/bar/{}/{}?bar=baz&fire={}&blob=blah",
                options=["foo", "fish"]
            )
        }
    )

    args = [
        pyargs.Argument(
            name="fire",
            description="blah",
            required=True,
            value="bright"
        ),
        pyargs.Argument(
            name="fish",
            description="blah",
            required=True,
            value="wet"
        ),
        pyargs.Argument(
            name="foo",
            description="blah",
            required=True,
            value="bar"
        )
    ]

    request = endpoint.build_request("foo", args)

    assert request.url == "https://www.google.com/foo/bar/bar/wet?bar=baz&fire=bright&blob=blah"
    assert request.method == "get"

def test_correctly_constructs_url_with_multiple_args_including_some_in_query():

    endpoint = Endpoint(
        name="foo",
        base_url="https://www.google.com",
        paths={
            "foo": Path(
                method="get",
                name="foo",
                route="foo/bar/{}/{}?fire={}",
                options=["foo", "fish"]
            )
        }
    )

    args = [
        pyargs.Argument(
            name="fire",
            description="blah",
            required=True,
            value="bright"
        ),
        pyargs.Argument(
            name="fish",
            description="blah",
            required=True,
            value="wet"
        ),
        pyargs.Argument(
            name="foo",
            description="blah",
            required=True,
            value="bar"
        )
    ]

    request = endpoint.build_request("foo", args)

    assert request.url == "https://www.google.com/foo/bar/bar/wet?fire=bright"
    assert request.method == "get"

def test_correctly_constructs_url_with_multiple_args():

    endpoint = Endpoint(
        name="foo",
        base_url="https://www.google.com",
        paths={
            "foo": Path(
                name="foo",
                method="get",
                options=["foo", "fish"],
                route="foo/bar/{}/{}"
            )
        }
    )

    args = [
        pyargs.Argument(
            name="fire",
            description="blah",
            required=True,
            value="bright"
        ),
        pyargs.Argument(
            name="fish",
            description="blah",
            required=True,
            value="wet"
        ),
        pyargs.Argument(
            name="foo",
            description="blah",
            required=True,
            value="bar"
        )
    ]

    request = endpoint.build_request("foo", args)

    assert request.url == "https://www.google.com/foo/bar/bar/wet"
    assert request.method == "get"
