from datetime import datetime

import pytest

from brutal_bag.models.wallabag_article_fetcher import WallabagArticleFetcher


@pytest.fixture(name="wallabag_article_fetcher")
def wallabag_article_fetcher_fixture(mocker, elvis_entry, yeti_entry):
    wallabag = mocker.AsyncMock()
    wallabag.get_unread_articles.return_value = [elvis_entry, yeti_entry]
    wallabag.get_unread_articles_by_tag.return_value = [yeti_entry]
    wallabag.get_article_count.return_value = 10
    wallabag.get_article_by_id.return_value = elvis_entry

    return WallabagArticleFetcher(wallabag)


@pytest.fixture(name="elvis_entry")
def elvis_entry_fixture():
    return {
        "id": 1,
        "title": "Elvis Presley is alive and living in a cave",
        "content": "A hobo wandering",
        "url": "https://www.example.com/1",
        "published_by": ["Hobo News"],
        "published_at": "2019-11-13T13:51:47-0700",
        "reading_time": 3,
        "tags": [{"id": "1", "label": "Cave", "slug": "cave"}],
    }


@pytest.fixture(name="yeti_entry")
def yeti_entry_fixture():
    return {
        "id": 2,
        "title": "A Yeti was seen on the New Jersey Turnpike",
        "content": "He wore Dock Martins...",
        "url": "https://www.yetinews.com/2",
        "published_by": ["Questionable Geographic"],
    }


def test_wallabag_entry_to_article(elvis_entry):
    article = WallabagArticleFetcher.wallabag_entry_to_article(elvis_entry)
    assert article
    assert article.id == "1"
    assert article.title == "Elvis Presley is alive and living in a cave"
    assert article.content == "A hobo wandering"
    assert article.external_url == "https://www.example.com/1"
    assert article.published_by == ["Hobo News"]
    assert article.date == datetime(2019, 11, 13, 20, 51, 47)
    assert article.reading_time == 3
    assert len(article.tags) == 1
    tag = article.tags[0]
    assert tag.id == "1"
    assert tag.label == "Cave"
    assert tag.slug == "cave"


def test_wallabag_entry_to_article_no_entry():
    article = WallabagArticleFetcher.wallabag_entry_to_article(None)
    assert article is None


async def test_get_all_unread(wallabag_article_fetcher):
    articles = await wallabag_article_fetcher.get_all_unread()
    assert len(articles) == 2
    assert articles[0].id == "1"
    assert articles[1].id == "2"


async def test_get_all_unread_by_tag(wallabag_article_fetcher):
    articles = await wallabag_article_fetcher.get_all_unread_by_tag("yeti")
    assert len(articles) == 1
    assert articles[0].id == "2"


async def test_get_by_id(wallabag_article_fetcher):
    article = await wallabag_article_fetcher.get_by_id("1")
    assert article.id == "1"
    assert article.title == "Elvis Presley is alive and living in a cave"


async def test_get_count(wallabag_article_fetcher):
    count = await wallabag_article_fetcher.get_count()
    assert count == 10
