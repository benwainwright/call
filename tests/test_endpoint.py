# import pyargs

# from call.endpoint import Endpoint


# def test_correctly_constructs_url_without_options():

#     endpoint = Endpoint(
#         name="foo",
#         base_url="https://www.google.com",
#         path_string="foo/bar",
#         path_name="foo",
#         method="get",
#         option_names=[],
#     )

#     url = endpoint.get_url()

#     assert url == "https://www.google.com/foo/bar"


# def test_correctly_constructs_url_with_single_arg():

#     endpoint = Endpoint(
#         name="foo",
#         base_url="https://www.google.com",
#         path_string="foo/bar/{}/bar",
#         path_name="foo",
#         method="get",
#         option_names=["foo"],
#     )

#     args = [
#         pyargs.Argument(
#             name="foo",
#             description="blah",
#             required=True,
#             value="baz"
#         )
#     ]

#     url = endpoint.get_url(args)

#     assert url == "https://www.google.com/foo/bar/baz/bar"

# def test_correctly_constructs_url_with_query_that_has_constant_parts():
#     endpoint = Endpoint(
#         name="foo",
#         base_url="https://www.google.com",
#         path_string="foo/bar/{}/{}?bar=baz&fire={}&blob=blah",
#         path_name="foo",
#         method="get",
#         option_names=["foo", "fish"],
#     )

#     args = [
#         pyargs.Argument(
#             name="fire",
#             description="blah",
#             required=True,
#             value="bright"
#         ),
#         pyargs.Argument(
#             name="fish",
#             description="blah",
#             required=True,
#             value="wet"
#         ),
#         pyargs.Argument(
#             name="foo",
#             description="blah",
#             required=True,
#             value="bar"
#         )
#     ]

#     url = endpoint.get_url(args)

#     assert url == "https://www.google.com/foo/bar/bar/wet?bar=baz&fire=bright&blob=blah"

# def test_correctly_constructs_url_with_multiple_args_including_some_in_query():

#     endpoint = Endpoint(
#         name="foo",
#         base_url="https://www.google.com",
#         path_string="foo/bar/{}/{}?fire={}",
#         path_name="foo",
#         method="get",
#         option_names=["foo", "fish"],
#     )

#     args = [
#         pyargs.Argument(
#             name="fire",
#             description="blah",
#             required=True,
#             value="bright"
#         ),
#         pyargs.Argument(
#             name="fish",
#             description="blah",
#             required=True,
#             value="wet"
#         ),
#         pyargs.Argument(
#             name="foo",
#             description="blah",
#             required=True,
#             value="bar"
#         )
#     ]

#     url = endpoint.get_url(args)

#     assert url == "https://www.google.com/foo/bar/bar/wet?fire=bright"

# def test_correctly_constructs_url_with_multiple_args():

#     endpoint = Endpoint(
#         name="foo",
#         base_url="https://www.google.com",
#         path_string="foo/bar/{}/{}",
#         path_name="foo",
#         method="get",
#         option_names=["foo", "fish"]
#     )

#     args = [
#         pyargs.Argument(
#             name="fire",
#             description="blah",
#             required=True,
#             value="bright"
#         ),
#         pyargs.Argument(
#             name="fish",
#             description="blah",
#             required=True,
#             value="wet"
#         ),
#         pyargs.Argument(
#             name="foo",
#             description="blah",
#             required=True,
#             value="bar"
#         )
#     ]

#     url = endpoint.get_url(args)

#     assert url == "https://www.google.com/foo/bar/bar/wet"
