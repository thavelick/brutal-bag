import os
import pytest
import time

from unittest.mock import AsyncMock, Mock
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
def wallabag_api_fixtrue():
    wallabag_api = AsyncMock()
    wallabag_api.get_entries.return_value = {"_embedded": {"items": []}}
    wallabag_api.get_tags.return_value = []
    return wallabag_api


async def test_missing_environment(wallabag):
    wallabag.get_environment = Mock(return_value={})
    with pytest.raises(MissingEnvironment):
        await wallabag.connect()


def test_get_environment():
    assert Wallabag().get_environment() == os.environ


async def test_connect(mocker, wallabag, wallabag_api):
    wallabag.wallabag_api = wallabag_api
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


async def test_get_unread_articles(wallabag, wallabag_api):
    wallabag.connect = AsyncMock()
    wallabag.wallabag_api = wallabag_api
    articles = await wallabag.get_unread_articles()
    assert articles == []


async def test_get_all_tags(wallabag, wallabag_api):
    wallabag.connect = AsyncMock()
    wallabag.wallabag_api = wallabag_api
    tags = await wallabag.get_all_tags()

    assert tags == []
