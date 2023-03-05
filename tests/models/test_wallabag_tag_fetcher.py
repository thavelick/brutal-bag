import pytest

from brutal_bag.models.wallabag_tag_fetcher import WallabagTagFetcher


@pytest.fixture(name="wallabag_tag_fetcher")
def wallabag_tag_fetcher_fixture(mocker):
    wallabag = mocker.AsyncMock()
    wallabag.get_article_count.return_value = 0
    wallabag.get_all_tags.return_value = [
        {"id": "1", "label": "Cave", "slug": "cave"},
        {"id": "2", "label": "Yeti", "slug": "yeti"},
    ]

    return WallabagTagFetcher(wallabag)


async def test_get_all(wallabag_tag_fetcher):
    tags = await wallabag_tag_fetcher.get_all()
    assert len(tags) == 2
    assert tags[0].id == "1"
    assert tags[0].label == "Cave"
    assert tags[0].slug == "cave"
    assert tags[0].unread_count == 0
    assert tags[1].id == "2"
    assert tags[1].label == "Yeti"
    assert tags[1].slug == "yeti"
    assert tags[1].unread_count == 0
