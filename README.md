# pythonsdk

An official Python SDK for [ScreenshotOne.com API](https://screenshotone.com) to take screenshots of URLs, render HTML as images and PDF.

It takes minutes to start taking screenshots. Just [sign up](https://screenshotone.com/) to get access and secret keys, import the client, and you are ready to go.

The SDK client is synchronized with the latest [screenshot API options](https://screenshotone.com/docs/options/).

## Installation

```shell
pip install screenshotone
```

## Usage

Generate a screenshot URL without executing the request. Or download the screenshot. It is up to you:

```python
import shutil
from screenshotone import Client, TakeOptions

# create API client
client = Client('<your access key>', '<your secret key>')

# set up options
options = (TakeOptions.url('https://screenshotone.com')
    .format("png")
    .viewport_width(1024)
    .viewport_height(768)
    .block_cookie_banners(True)
    .block_chats(True))

# generate the screenshot URL and share it with a user
url = client.generate_take_url(options)
# expected output: https://api.screenshotone.com/take?url=https%3A%2F%2Fscreenshotone.com&viewport_width=1024&viewport_height=768&block_cookie_banners=True&block_chats=True&access_key=<your access key>&signature=6afc9417a523788580fa01a9f668ea82c78a9d2b41441d2a696010bf2743170f

# or render a screenshot and download the image as stream
image = client.take(options)

# store the screenshot the example.png file
with open('example.png', 'wb') as result_file:
    shutil.copyfileobj(image, result_file)
```

### How to handle errors

Read about [how to handle the ScreenshotOne API errors](https://screenshotone.com/docs/guides/how-to-handle-api-errors/), and that's how you can get the HTTP status code and the error code of the request:

```python
try:
    # ...
    # render a screenshot and download the image as stream
    image = client.take(options)
    # ...
except InvalidRequestException as e:
    print(f"Invalid request: {e}")
    if e.http_status_code:
        print(f"HTTP Status Code: {e.http_status_code}")
    if e.error_code:
        print(f"Error Code: {e.error_code}")
except APIErrorException as e:
    print(f"API Error: {e}")
    if e.http_status_code:
        print(f"HTTP Status Code: {e.http_status_code}")
    if e.error_code:
        print(f"Error Code: {e.error_code}")
except Exception as e:
    # handle any other exceptions
    print(f"An unexpected error occurred: {e}")
```

## Release

[Github Actions](https://github.com/screenshotone/pythonsdk/blob/main/.github/workflows/pypi-release.yml) is used to automate the release process and publishing to PyPI. Update the library version in `pyproject.toml` and [create a new release](https://github.com/screenshotone/pythonsdk/releases/new) to launch the `publish` workflow.

## License

`screenshotone/pythonsdk` is released under [the MIT license](LICENSE).
