import io
import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

from screenshotone import Client, TakeOptions


DOCUMENTATION = json.loads(
    (Path(__file__).parent / "fixtures" / "documented_options.json").read_text()
)


class DocumentedOptionsTests(unittest.TestCase):
    def test_documented_options_have_helpers_with_correct_api_names(self):
        # The independent snapshot comes from the public option reference.
        # Authentication is supplied by Client; async is a Python keyword.
        for name in DOCUMENTATION["options"]:
            if name == "access_key":
                continue
            with self.subTest(option=name):
                value = "option-value"
                if name in ("url", "html", "markdown"):
                    options = getattr(TakeOptions, name)(value)
                else:
                    options = TakeOptions({})
                    method_name = "async_option" if name == "async" else name
                    self.assertIs(getattr(options, method_name)(value), options)

                self.assertEqual(options.query(), {name: value})

    def new_options(self):
        options = TakeOptions.url("https://example.com")
        for name, value in DOCUMENTATION["new_option_examples"].items():
            getattr(options, name)(value)
        return options

    def test_new_options_survive_url_encoding_including_repeated_values(self):
        client = Client("test-access-key", "test-secret-key")
        options = self.new_options()

        query = parse_qs(urlsplit(client.generate_take_url(options)).query)

        for name, value in DOCUMENTATION["new_option_examples"].items():
            with self.subTest(option=name):
                values = value if isinstance(value, list) else [value]
                self.assertEqual(query[name], [str(item) for item in values])
        self.assertEqual(query["url"], ["https://example.com"])
        self.assertEqual(query["access_key"], ["test-access-key"])
        self.assertEqual(len(query["signature"]), 1)

    def test_new_options_reach_streaming_requests_with_original_json_types(self):
        client = Client("test-access-key", "test-secret-key")
        options = self.new_options()
        stream = io.BytesIO(b"mocked screenshot")
        response = SimpleNamespace(status_code=200, headers={}, raw=stream)
        expected_query = {"url": "https://example.com"}
        expected_query.update(DOCUMENTATION["new_option_examples"])
        expected_query["access_key"] = "test-access-key"

        for method_name in ("take", "take_with_metadata"):
            with self.subTest(method=method_name), patch(
                "screenshotone.sdk.requests.post", return_value=response
            ) as post:
                result = getattr(client, method_name)(options)

                post.assert_called_once_with(
                    "https://api.screenshotone.com/take",
                    json=expected_query,
                    stream=True,
                )
                screenshot = result if method_name == "take" else result.screenshot
                self.assertIs(screenshot, stream)


if __name__ == "__main__":
    unittest.main()
