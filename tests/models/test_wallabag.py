import os
import pytest
import time

from brutal_bag.models.wallabag import Wallabag, MissingEnvironment


@pytest.fixture(name="wallabag")
def wallabag_fixture(mocker):
    mocker.patch.object(
        Wallabag,
        "get_environment",
        return_value={
            "WALLABAG_CLIENT_ID": "dummy_client_id",
            "WALLABAG_CLIENT_SECRET": "dummy_client_secret",
            "WALLABAG_PASSWORD": "dummy_password",
            "WALLABAG_URL": "http://dummy.url",
            "WALLABAG_USERNAME": "dummy_username",
        },
    )
    return Wallabag()


@pytest.fixture(name="wallabag_api")
def wallabag_api_fixtrue(mocker):
    wallabag_api = mocker.AsyncMock()
    wallabag_api.get_entries.return_value = {"_embedded": {"items": []}, "total": 10}
    wallabag_api.get_tags.return_value = []
    wallabag_api.get_entry.return_value = {}
    return wallabag_api


@pytest.fixture(name="connected_wallabag")
def connected_wallabag_fixture(mocker, wallabag, wallabag_api):
    wallabag.wallabag_api = wallabag_api
    wallabag.connect = mocker.AsyncMock()
    return wallabag


async def test_missing_environment(mocker, wallabag):
    wallabag.get_environment = mocker.Mock(return_value={})
    with pytest.raises(MissingEnvironment):
        await wallabag.connect()


def test_get_environment():
    assert Wallabag().get_environment() == os.environ


async def test_connect(mocker, wallabag):
    mocker.patch(
        "brutal_bag.models.wallabag.WallabagAPI.get_token", return_value="dummy_token"
    )

    await wallabag.connect()

    assert wallabag.token == "dummy_token"
    assert wallabag.token_expires_at > time.time()


async def test_connect_with_existing_token(wallabag):
    wallabag.token = "dummy_token"
    expiry = time.time() + 3600
    wallabag.token_expires_at = expiry

    await wallabag.connect()

    assert wallabag.token == "dummy_token"
    assert wallabag.token_expires_at == expiry


@pytest.mark.parametrize(
    "params, expected_params",
    [
        (
            {"unread": True, "tag": "sample", "per_page": 30},
            {"archive": 0, "page": 1, "perPage": 30, "tags": ["sample"]},
        ),
        (
            {"unread": False, "tag": None, "per_page": 50},
            {"archive": 1, "page": 1, "perPage": 50},
        ),
        (
            {"unread": True, "tag": None, "per_page": 20},
            {"archive": 0, "page": 1, "perPage": 20},
        ),
        (
            {"unread": True, "tag": "sample"},
            {"archive": 0, "page": 1, "perPage": 30, "tags": ["sample"]},
        ),
        ({"unread": False, "tag": None}, {"archive": 1, "page": 1, "perPage": 30}),
        ({"unread": True, "tag": None}, {"archive": 0, "page": 1, "perPage": 30}),
    ],
)
async def test_get_articles(connected_wallabag, wallabag_api, params, expected_params):
    articles = await connected_wallabag.get_articles(**params)

    wallabag_api.get_entries.assert_called_once_with(**expected_params)

    assert articles == []


async def test_get_artice_by_id(connected_wallabag):
    article = await connected_wallabag.get_article_by_id(1)

    assert article == {}


async def test_get_all_tags(connected_wallabag):
    tags = await connected_wallabag.get_all_tags()

    assert tags == []


async def test_get_article_count(connected_wallabag):
    count = await connected_wallabag.get_article_count(unread=True, tag="sample")

    assert count == 10
