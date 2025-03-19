from collections import OrderedDict
from typing import List
import urllib.parse
import hmac
import hashlib
import requests
import json

API_BASE_URL = "https://api.screenshotone.com"
API_TAKE_PATH = "/take"


class InvalidRequestException(Exception):
    def __init__(
        self, message, http_status_code=None, error_code=None, documentation_url=None
    ):
        self.http_status_code = http_status_code
        self.error_code = error_code
        self.documentation_url = documentation_url

        super().__init__(message)


class APIErrorException(Exception):
    def __init__(
        self, message, http_status_code=None, error_code=None, documentation_url=None
    ):
        self.http_status_code = http_status_code
        self.error_code = error_code
        self.documentation_url = documentation_url
        super().__init__(message)


class TakeOptions:
    options = OrderedDict()

    def __init__(self, defaults):
        for key, value in defaults.items():
            self.options[key] = value

    def url(url):
        return TakeOptions({"url": url})

    def html(html):
        return TakeOptions({"html": html})

    def markdown(markdown):
        return TakeOptions({"markdown": markdown})

    def signature(self, value):
        self.options["signature"] = value

        return self

    def selector(self, value):
        self.options["selector"] = value

        return self

    def error_on_selector_not_found(self, value):
        self.options["error_on_selector_not_found"] = value

        return self

    def response_type(self, value):
        self.options["response_type"] = value

        return self

    def openai_api_key(self, value):
        self.options["openai_api_key"] = value

        return self

    def vision_prompt(self, value):
        self.options["vision_prompt"] = value

        return self

    def ip_country_code(self, value):
        self.options["ip_country_code"] = value

        return self

    def vision_max_tokens(self, value):
        self.options["vision_max_tokens"] = value

        return self

    def format(self, value):
        self.options["format"] = value

        return self

    def clip_x(self, value):
        self.options["clip_x"] = value

        return self

    def clip_y(self, value):
        self.options["clip_y"] = value

        return self

    def clip_width(self, value):
        self.options["clip_width"] = value

        return self

    def clip_height(self, value):
        self.options["clip_height"] = value

        return self

    def dark_mode(self, value):
        self.options["dark_mode"] = value

        return self

    def reduced_motion(self, value):
        self.options["reduced_motion"] = value

        return self

    def media_type(self, value):
        self.options["media_type"] = value

        return self

    def scripts(self, value):
        self.options["scripts"] = value

        return self

    def scripts_wait_until(self, value):
        self.options["scripts_wait_until"] = value

        return self

    def styles(self, value):
        self.options["styles"] = value

        return self

    def hide_selectors(self, values: List[str]):
        self.options["hide_selectors"] = values

        return self

    def click(self, value):
        self.options["click"] = value

        return self

    def image_quality(self, value):
        self.options["image_quality"] = value

        return self

    def image_width(self, value):
        self.options["image_width"] = value

        return self

    def image_height(self, value):
        self.options["image_height"] = value

        return self

    def omit_background(self, value):
        self.options["omit_background"] = value

        return self

    def viewport_device(self, value):
        self.options["viewport_device"] = value

        return self

    def viewport_width(self, value):
        self.options["viewport_width"] = value

        return self

    def viewport_height(self, value):
        self.options["viewport_height"] = value

        return self

    def device_scale_factor(self, value):
        self.options["device_scale_factor"] = value

        return self

    def viewport_mobile(self, value):
        self.options["viewport_mobile"] = value

        return self

    def viewport_has_touch(self, value):
        self.options["viewport_has_touch"] = value

        return self

    def viewport_landscape(self, value):
        self.options["viewport_landscape"] = value

        return self

    def full_page(self, value):
        self.options["full_page"] = value

        return self

    def full_page_scroll(self, value):
        self.options["full_page_scroll"] = value

        return self

    def fail_if_content_contains(self, value):
        self.options["fail_if_content_contains"] = value

        return self

    def full_page_scroll_delay(self, value):
        self.options["full_page_scroll_delay"] = value

        return self

    def full_page_max_height(self, value):
        self.options["full_page_max_height"] = value

        return self

    def full_page_scroll_by(self, value):
        self.options["full_page_scroll_by"] = value

        return self

    def geolocation_latitude(self, value):
        self.options["geolocation_latitude"] = value

        return self

    def geolocation_longitude(self, value):
        self.options["geolocation_longitude"] = value

        return self

    def geolocation_accuracy(self, value):
        self.options["geolocation_accuracy"] = value

        return self

    def block_cookie_banners(self, value):
        self.options["block_cookie_banners"] = value

        return self

    def block_banners_by_heuristics(self, value):
        self.options["block_banners_by_heuristics"] = value

        return self

    def block_chats(self, value):
        self.options["block_chats"] = value

        return self

    def block_ads(self, value):
        self.options["block_ads"] = value

        return self

    def block_socials(self, value):
        self.options["block_socials"] = value

        return self

    def block_trackers(self, value):
        self.options["block_trackers"] = value

        return self

    def block_requests(self, values: List[str]):
        self.options["block_requests"] = values

        return self

    def block_resources(self, values: List[str]):
        self.options["block_resources"] = values

        return self

    def cache(self, value):
        self.options["cache"] = value

        return self

    def cache_ttl(self, value):
        self.options["cache_ttl"] = value

        return self

    def cache_key(self, value):
        self.options["cache_key"] = value

        return self

    def user_agent(self, value):
        self.options["user_agent"] = value

        return self

    def authorization(self, value):
        self.options["authorization"] = value

        return self

    def headers(self, values: List[str]):
        self.options["headers"] = values

        return self

    def cookies(self, values: List[str]):
        self.options["cookies"] = values

        return self

    def proxy(self, value):
        self.options["proxy"] = value

        return self

    def time_zone(self, value):
        self.options["time_zone"] = value

        return self

    def delay(self, value):
        self.options["delay"] = value

        return self

    def timeout(self, value):
        self.options["timeout"] = value

        return self

    def wait_until(self, values: List[str]):
        self.options["wait_until"] = values

        return self

    def wait_for_selector(self, value):
        self.options["wait_for_selector"] = value

        return self

    def store(self, value):
        self.options["store"] = value

        return self

    def storage_bucket(self, value):
        self.options["storage_bucket"] = value

        return self

    def storage_path(self, value):
        self.options["storage_path"] = value

        return self

    def storage_class(self, value):
        self.options["storage_class"] = value

        return self

    def storage_acl(self, value):
        self.options["storage_acl"] = value

        return self

    def storage_endpoint(self, value):
        self.options["storage_endpoint"] = value

        return self

    def storage_access_key_id(self, value):
        self.options["storage_access_key_id"] = value

        return self

    def storage_secret_access_key(self, value):
        self.options["storage_secret_access_key"] = value

        return self

    def storage_return_location(self, value):
        self.options["storage_return_location"] = value

        return self

    def metadata_image_size(self, value):
        self.options["metadata_image_size"] = value

        return self

    def metadata_fonts(self, value):
        self.options["metadata_fonts"] = value

        return self

    def metadata_icon(self, value):
        self.options["metadata_icon"] = value

        return self

    def metadata_open_graph(self, value):
        self.options["metadata_open_graph"] = value

        return self

    def metadata_page_title(self, value):
        self.options["metadata_page_title"] = value

        return self

    def metadata_content(self, value):
        self.options["metadata_content"] = value

        return self

    def metadata_http_response_status_code(self, value):
        self.options["metadata_http_response_status_code"] = value

        return self

    def metadata_http_response_headers(self, value):
        self.options["metadata_http_response_headers"] = value

        return self

    def async_option(self, value):
        self.options["async"] = value

        return self

    def webhook_url(self, value):
        self.options["webhook_url"] = value

        return self

    def webhook_sign(self, value):
        self.options["webhook_sign"] = value

        return self

    def ignore_host_errors(self, value):
        self.options["ignore_host_errors"] = value

        return self

    def error_on_click_selector_not_found(self, value):
        self.options["error_on_click_selector_not_found"] = value

        return self

    def fail_if_gpu_rendering_fails(self, value):
        self.options["fail_if_gpu_rendering_fails"] = value

        return self

    def selector_scroll_into_view(self, value):
        self.options["selector_scroll_into_view"] = value

        return self

    def capture_beyond_viewport(self, value):
        self.options["capture_beyond_viewport"] = value

        return self

    def scroll_into_view(self, value):
        self.options["scroll_into_view"] = value

        return self

    def scroll_into_view_adjust_top(self, value):
        self.options["scroll_into_view_adjust_top"] = value

        return self

    def request_gpu_rendering(self, value):
        self.options["request_gpu_rendering"] = value

        return self

    def pdf_print_background(self, value):
        self.options["pdf_print_background"] = value

        return self

    def pdf_fit_one_page(self, value):
        self.options["pdf_fit_one_page"] = value

        return self

    def pdf_landscape(self, value):
        self.options["pdf_landscape"] = value

        return self

    def pdf_paper_format(self, value):
        self.options["pdf_paper_format"] = value

        return self

    def bypass_csp(self, value):
        self.options["bypass_csp"] = value

        return self

    def navigation_timeout(self, value):
        self.options["navigation_timeout"] = value

        return self

    def wait_for_selector_algorithm(self, value):
        self.options["wait_for_selector_algorithm"] = value

        return self

    def full_page_algorithm(self, value):
        self.options["full_page_algorithm"] = value

        return self

    def query(self):
        return self.options


class ScreenshotResultVision:
    completion = None


class ScreenshotResult:
    screenshot = None
    vision = None


class Client:
    access_key = None
    secret_key = None

    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key
        self.secret_key = secret_key

    def with_keys(access_key: str, secret_key: str):
        return Client(access_key, secret_key)

    def generate_take_url(self, options: TakeOptions):
        query = options.query()
        query["access_key"] = self.access_key

        query_string = urllib.parse.urlencode(query, doseq=True)

        signature = hmac.new(
            bytes(self.secret_key, "utf-8"),
            msg=bytes(query_string, "utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

        return "%s%s?%s&signature=%s" % (
            API_BASE_URL,
            API_TAKE_PATH,
            query_string,
            signature,
        )

    def take(self, options):
        query = options.query()
        query["access_key"] = self.access_key

        url = "%s%s" % (API_BASE_URL, API_TAKE_PATH)
        r = requests.post(url, json=query, stream=True)

        if r.status_code == 200:
            return r.raw
        elif r.status_code == 400:
            error_response = json.loads(r.text)
            if not error_response.get("is_successful"):
                error_response = json.loads(r.text)
                error_messages = [
                    detail["message"]
                    for detail in error_response.get("error_details", [])
                ]
                error_message = (
                    f"Error: {error_response.get('error_message', 'Unknown error')}\n"
                )
                error_message += "\n".join(error_messages)
                error_code = error_response.get("error_code")
                documentation_url = error_response.get("documentation_url")

                raise InvalidRequestException(
                    error_message,
                    http_status_code=r.status_code,
                    error_code=error_code,
                    documentation_url=documentation_url,
                )
        else:
            error_response = json.loads(r.text)
            error_code = error_response.get("error_code")
            documentation_url = error_response.get("documentation_url")
            error_message = f"An error occurred while processing the request. Status code: {r.status_code}, error code: {error_code}"

            raise APIErrorException(
                error_message,
                http_status_code=r.status_code,
                error_code=error_code,
                documentation_url=documentation_url,
            )

        return None

    def take_with_metadata(self, options):
        query = options.query()
        query["access_key"] = self.access_key

        url = "%s%s" % (API_BASE_URL, API_TAKE_PATH)
        r = requests.post(url, json=query, stream=True)

        vision = None
        completion = r.headers.get("x-screenshotone-vision-completion")
        if completion is not None:
            vision = ScreenshotResultVision(completion=completion)

        if r.status_code == 200:
            return ScreenshotResult(screenshot=r.raw, vision=vision)
        elif r.status_code == 400:
            error_response = json.loads(r.text)
            if not error_response.get("is_successful"):
                error_messages = [
                    detail["message"]
                    for detail in error_response.get("error_details", [])
                ]
                error_message = (
                    f"Error: {error_response.get('error_message', 'Unknown error')}\n"
                )
                error_message += "\n".join(error_messages)
                error_code = error_response.get("error_code")
                documentation_url = error_response.get("documentation_url")

                raise InvalidRequestException(
                    error_message,
                    http_status_code=r.status_code,
                    error_code=error_code,
                    documentation_url=documentation_url,
                )
        else:
            error_response = json.loads(r.text)
            error_code = error_response.get("error_code")
            documentation_url = error_response.get("documentation_url")
            error_message = f"An error occurred while processing the request. Status code: {r.status_code}, error code: {error_code}"

            raise APIErrorException(
                error_message,
                http_status_code=r.status_code,
                error_code=error_code,
                documentation_url=documentation_url,
            )

        return None
