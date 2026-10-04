import hashlib
import hmac
import io
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from screenshotone import Client, TakeOptions
from screenshotone.sdk import APIErrorException, InvalidRequestException


class TakeOptionsTests(unittest.TestCase):
    def test_second_request_does_not_change_first_screenshot_url(self):
        client = Client("test-access-key", "test-secret-key")
        first = TakeOptions.url("https://example.com/first").format("png")
        second = TakeOptions.url("https://example.com/second").format("jpeg")

        first_query = parse_qs(urlsplit(client.generate_take_url(first)).query)
        second_query = parse_qs(urlsplit(client.generate_take_url(second)).query)

        self.assertEqual(first_query["url"], ["https://example.com/first"])
        self.assertEqual(first_query["format"], ["png"])
        self.assertEqual(second_query["url"], ["https://example.com/second"])
        self.assertEqual(second_query["format"], ["jpeg"])

    def test_new_input_does_not_inherit_previous_request_options(self):
        factories = (
            ("url", "https://example.com/second"),
            ("html", "<p>Second request</p>"),
            ("markdown", "# Second request"),
        )
        for input_name, value in factories:
            with self.subTest(input=input_name):
                first = TakeOptions.url("https://example.com/first").format("png")
                second = getattr(TakeOptions, input_name)(value)

                self.assertEqual(second.query(), {input_name: value})
                self.assertIsNot(first.query(), second.query())


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.client = Client("test-access-key", "test-secret-key")
        self.options = TakeOptions.url("https://example.com")
        self.stream = io.BytesIO(b"mocked screenshot")

    def response(self, headers=None, status_code=200, text=""):
        return SimpleNamespace(
            status_code=status_code,
            headers=headers if headers is not None else {},
            raw=self.stream,
            text=text,
        )

    @patch("screenshotone.sdk.requests.post")
    def test_take_returns_original_raw_stream(self, post):
        post.return_value = self.response()
        expected_query = self.options.query().copy()
        expected_query["access_key"] = "test-access-key"

        self.assertIs(self.client.take(self.options), self.stream)
        post.assert_called_once_with(
            "https://api.screenshotone.com/take",
            json=expected_query,
            stream=True,
        )

    @patch("screenshotone.sdk.requests.post")
    def test_take_with_metadata_without_vision_returns_screenshot(self, post):
        post.return_value = self.response()

        result = self.client.take_with_metadata(self.options)

        self.assertIs(result.screenshot, self.stream)
        self.assertIsNone(result.vision)

    @patch("screenshotone.sdk.requests.post")
    def test_take_with_metadata_returns_vision_completion(self, post):
        for completion in ("synthetic vision completion", ""):
            with self.subTest(completion=completion):
                post.return_value = self.response(
                    {"x-screenshotone-vision-completion": completion}
                )

                result = self.client.take_with_metadata(self.options)

                self.assertIs(result.screenshot, self.stream)
                self.assertEqual(result.vision.completion, completion)

    def test_client_operations_do_not_mutate_caller_options(self):
        for method_name in ("generate_take_url", "take", "take_with_metadata"):
            with self.subTest(method=method_name):
                options = TakeOptions(
                    {"url": "https://example.com", "access_key": "caller-owned-value"}
                )
                original = options.query().copy()
                with patch(
                    "screenshotone.sdk.requests.post", return_value=self.response()
                ):
                    getattr(self.client, method_name)(options)

                self.assertEqual(options.query(), original)

    def test_signed_url_signs_exact_boolean_query_without_mutating_options(self):
        options = TakeOptions.url("https://example.com").full_page(True).cache(False)
        expected_query = (
            "url=https%3A%2F%2Fexample.com&full_page=True&cache=False"
            "&access_key=test-access-key"
        )
        expected_signature = hmac.new(
            b"test-secret-key", expected_query.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        self.assertEqual(
            self.client.generate_take_url(options),
            "https://api.screenshotone.com/take?"
            + expected_query
            + "&signature="
            + expected_signature,
        )
        self.assertEqual(
            options.query(),
            {"url": "https://example.com", "full_page": True, "cache": False},
        )

    def test_http_errors_keep_status_and_api_details(self):
        error_body = json.dumps(
            {
                "is_successful": False,
                "error_message": "Mock API error",
                "error_code": "mock_error",
                "documentation_url": "https://example.com/errors/mock_error",
                "returned_status_code": 403,
            }
        )
        for method_name in ("take", "take_with_metadata"):
            for status, error_type in (
                (400, InvalidRequestException),
                (500, APIErrorException),
            ):
                with self.subTest(method=method_name, status=status):
                    response = self.response(status_code=status, text=error_body)
                    with patch(
                        "screenshotone.sdk.requests.post", return_value=response
                    ), self.assertRaises(error_type) as raised:
                        getattr(self.client, method_name)(self.options)

                    self.assertEqual(raised.exception.http_status_code, status)
                    self.assertEqual(raised.exception.error_code, "mock_error")
                    self.assertEqual(
                        raised.exception.documentation_url,
                        "https://example.com/errors/mock_error",
                    )
                    self.assertEqual(raised.exception.host_returned_status_code, 403)

    def test_http_400_raises_even_when_body_reports_success(self):
        response = self.response(
            status_code=400, text=json.dumps({"is_successful": True})
        )
        for method_name in ("take", "take_with_metadata"):
            with self.subTest(method=method_name):
                with patch(
                    "screenshotone.sdk.requests.post", return_value=response
                ), self.assertRaises(InvalidRequestException) as raised:
                    getattr(self.client, method_name)(self.options)

                self.assertEqual(raised.exception.http_status_code, 400)

    def test_non_json_error_bodies_raise_sdk_errors(self):
        cases = (
            (502, "<html>Bad Gateway</html>", APIErrorException),
            (503, "", APIErrorException),
            (400, "Invalid request", InvalidRequestException),
        )
        for method_name in ("take", "take_with_metadata"):
            for status, body, error_type in cases:
                with self.subTest(method=method_name, status=status):
                    response = self.response(status_code=status, text=body)
                    with patch(
                        "screenshotone.sdk.requests.post", return_value=response
                    ), self.assertRaises(error_type) as raised:
                        getattr(self.client, method_name)(self.options)

                    self.assertEqual(raised.exception.http_status_code, status)
                    self.assertIsNone(raised.exception.error_code)

    def test_non_object_json_error_bodies_raise_sdk_errors(self):
        for method_name in ("take", "take_with_metadata"):
            for body in ("null", "[]", '"error"', "42"):
                with self.subTest(method=method_name, body=body):
                    response = self.response(status_code=502, text=body)
                    with patch(
                        "screenshotone.sdk.requests.post", return_value=response
                    ), self.assertRaises(APIErrorException) as raised:
                        getattr(self.client, method_name)(self.options)

                    self.assertEqual(raised.exception.http_status_code, 502)

    def test_invalid_request_details_are_preserved(self):
        body = json.dumps(
            {
                "error_message": "Invalid options",
                "error_details": [
                    {"message": "Missing URL"},
                    {"message": "Invalid format"},
                ],
            }
        )
        for method_name in ("take", "take_with_metadata"):
            with self.subTest(method=method_name):
                response = self.response(status_code=400, text=body)
                with patch(
                    "screenshotone.sdk.requests.post", return_value=response
                ), self.assertRaises(InvalidRequestException) as raised:
                    getattr(self.client, method_name)(self.options)

                self.assertEqual(
                    str(raised.exception),
                    "Error: Invalid options\nMissing URL\nInvalid format",
                )

    def test_api_errors_can_be_caught_with_public_api_error_exception(self):
        from screenshotone import (
            APIErrorException as PublicAPIErrorException,
            InvalidRequestException as PublicInvalidRequestException,
        )

        self.assertIs(PublicAPIErrorException, APIErrorException)
        self.assertIs(PublicInvalidRequestException, InvalidRequestException)
        for method_name in ("take", "take_with_metadata"):
            for status, error_type in (
                (400, InvalidRequestException),
                (500, APIErrorException),
            ):
                with self.subTest(method=method_name, status=status):
                    response = self.response(status_code=status, text="{}")
                    with patch(
                        "screenshotone.sdk.requests.post", return_value=response
                    ), self.assertRaises(PublicAPIErrorException) as raised:
                        getattr(self.client, method_name)(self.options)

                    self.assertIsInstance(raised.exception, error_type)
                    self.assertEqual(raised.exception.http_status_code, status)


if __name__ == "__main__":
    unittest.main()
