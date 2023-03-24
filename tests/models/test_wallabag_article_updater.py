import pytest
from unittest.mock import AsyncMock

from brutal_bag.models.wallabag_article_updater import WallabagArticleUpdater


@pytest.fixture(name="wallabag")
def wallabag_fixture():
    wallabag = AsyncMock()
    wallabag.set_article_read.return_value = None
    wallabag.set_article_starred.return_value = None

    return wallabag


@pytest.fixture(name="wallabag_article_updater")
def wallabag_article_updater_fixture(wallabag):
    return WallabagArticleUpdater(wallabag)


async def test_update_read_state(wallabag, wallabag_article_updater):
    article_id = 1
    is_read = True

    await wallabag_article_updater.update_read_state(article_id, is_read)
    wallabag.set_article_read.assert_called_once_with(article_id, is_read)


async def test_update_starred_state(wallabag, wallabag_article_updater):
    article_id = 1
    is_starred = True

    await wallabag_article_updater.update_starred_state(article_id, is_starred)
    wallabag.set_article_starred.assert_called_once_with(article_id, is_starred)
