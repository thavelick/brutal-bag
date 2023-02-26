import pytest

from brutal_bag.models.wallabag_tag_fetcher import WallabagTagFetcher


@pytest.fixture(name="wallabag_tag_fetcher")
def wallabag_tag_fetcher_fixture():
    class MockWallabag:
        async def get_article_count(self, unread=True, tag=None):
            return 0

        async def get_unread_articles(self):
            return []

        async def get_all_tags(self):
            return [
                {"id": "1", "label": "Cave", "slug": "cave"},
                {"id": "2", "label": "Yeti", "slug": "yeti"},
            ]

    return WallabagTagFetcher(MockWallabag())


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
