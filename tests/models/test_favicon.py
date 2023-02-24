from unittest import mock

import httpx
import pytest

from brutal_bag.models.favicon import get_favicon_url


@mock.patch("httpx.get")
def test_get_favicon_url_with_valid_url(mock_get):
    mock_response = mock.MagicMock()
    mock_response.text = '<html><head><link rel="shortcut icon" href="/favicon.ico"></head><body></body></html>'
    mock_get.return_value = mock_response

    url = "https://www.example.com"
    assert get_favicon_url(url) == "https://www.example.com/favicon.ico"


@mock.patch("httpx.get")
def test_get_favicon_url_with_invalid_url(mock_get):
    mock_get.side_effect = httpx.ConnectError("Failed to connect")

    url = "https://invalid.url"
    assert get_favicon_url(url) is None


@mock.patch("httpx.head")
def test_get_favicon_url_with_empty_favicon(mock_head):
    mock_response = mock.MagicMock()
    mock_response.headers.get.return_value = "0"
    mock_head.return_value = mock_response

    url = "https://www.example.com"
    assert get_favicon_url(url) is None


@mock.patch("httpx.get")
@mock.patch("httpx.head")
def test_page_has_no_link_tag_but_has_default_favicon(mock_head, mock_get):
    # set up mock http response that does not have any link tag
    mock_get_response = mock.MagicMock()
    mock_get_response.text = "<html><head></head><body></body></html>"
    mock_get.return_value = mock_get_response

    # set up mock http response for standard favicon URL
    mock_head_response = mock.MagicMock()
    mock_head_response.headers.get.return_value = "1"
    mock_head.return_value = mock_head_response

    assert (
        get_favicon_url("https://example.com/article")
        == "https://example.com/favicon.ico"
    )


@mock.patch("httpx.get")
@mock.patch("httpx.head")
def test_page_has_no_link_and_default_favicon_error(mock_head, mock_get):
    # set up mock http response that does not have any link tag
    mock_get_response = mock.MagicMock()
    mock_get_response.text = "<html><head></head><body></body></html>"
    mock_get.return_value = mock_get_response

    # set up mock http response for standard favicon URL
    mock_head.side_effect = httpx.ConnectError("Failed to connect")

    assert get_favicon_url("https://example.com/article") is None
