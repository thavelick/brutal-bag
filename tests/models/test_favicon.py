import httpx

from brutal_bag.models.favicon import get_favicon_url


def test_get_favicon_url_with_valid_url(mocker):
    mock_response = mocker.Mock()
    mock_response.text = '<link rel="shortcut icon" href="/favicon.foo">'
    mocker.patch("httpx.get", return_value=mock_response)

    assert (
        get_favicon_url("https://www.example.com")
        == "https://www.example.com/favicon.foo"
    )


def test_get_favicon_url_with_invalid_url(mocker):
    mocker.patch("httpx.get", side_effect=httpx.ConnectError("Failed to connect"))

    assert get_favicon_url("https://invalid.url") is None


def test_get_favicon_url_with_empty_favicon(mocker):
    mock_get_response = mocker.Mock()
    mock_get_response.text = "nothing special"
    mocker.patch("httpx.get", return_value=mock_get_response)

    mock_head_response = mocker.Mock()
    mock_head_response.headers = {"content-length": "0"}
    mocker.patch("httpx.head", return_value=mock_head_response)

    assert get_favicon_url("https://www.example.com") is None


def test_page_has_no_link_tag_but_has_default_favicon(mocker):
    # set up mock http response that does not have any link tag
    mock_get_response = mocker.Mock()
    mock_get_response.text = "<html><head></head><body></body></html>"
    mocker.patch("httpx.get", return_value=mock_get_response)

    # set up mock http response for standard favicon URL
    mock_head_response = mocker.Mock()
    mock_head_response.headers = {"content-length": "123"}
    mocker.patch("httpx.head", return_value=mock_head_response)

    assert (
        get_favicon_url("https://example.com/article")
        == "https://example.com/favicon.ico"
    )


def test_page_has_no_link_and_default_favicon_error(mocker):
    # set up mock http response that does not have any link tag
    mock_get_response = mocker.Mock()
    mock_get_response.text = "<html><head></head><body></body></html>"

    mocker.patch("httpx.get", return_value=mock_get_response)
    # set up mock http response to error for standard favicon URL
    mocker.patch("httpx.head", side_effect=httpx.ConnectError("Failed to connect"))

    assert get_favicon_url("https://example.com/article") is None
