import httpx
from pytest_httpx import HTTPXMock

from brutal_bag.models.favicon import get_favicon_url


async def test_get_favicon_url_with_valid_url(httpx_mock):
    url = "https://www.example.com"
    response_text = '<link rel="shortcut icon" href="/favicon.foo">'
    httpx_mock.add_response(method="GET", text=response_text)

    assert await get_favicon_url(url) == f"{url}/favicon.foo"


async def test_get_favicon_url_with_invalid_url(httpx_mock: HTTPXMock):
    httpx_mock.add_exception(httpx.ConnectError("Failed to connect"))
    assert await get_favicon_url("https://invalid.url") is None


async def test_get_favicon_url_with_empty_favicon(httpx_mock):
    httpx_mock.add_response(method="GET", text="nothing special")
    httpx_mock.add_response(method="HEAD", headers={"content-length": "0"})

    assert await get_favicon_url("https://www.example.com") is None


async def test_page_has_no_link_tag_but_has_default_favicon(httpx_mock):
    httpx_mock.add_response(
        method="GET", text="<html><head></head><body></body></html>"
    )
    httpx_mock.add_response(method="HEAD", headers={"content-length": "123"})

    assert (
        await get_favicon_url("https://example.com/article")
        == "https://example.com/favicon.ico"
    )


async def test_page_has_no_link_and_default_favicon_error(httpx_mock):
    httpx_mock.add_response(
        method="GET", text="<html><head></head><body></body></html>"
    )
    httpx_mock.add_exception(httpx.ConnectError("Failed to connect"))

    assert await get_favicon_url("https://example.com/article") is None
