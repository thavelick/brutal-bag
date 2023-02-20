from datetime import datetime

import pytest

from brutal_bag.models.article import Article


@pytest.fixture(name="article")
def article_fixture():
    return Article(
        id="1",
        title="Elvis Presley is alive and living in a cave",
        content="A hobo wandering",
        external_url="https://www.example.com/1",
        published_by=["Hobo News"],
        date=datetime(2019, 11, 13, 13, 51, 47),
        reading_time=3,
        tags=["cave", "elvis"],
    )


def test_create(article):
    assert article
    assert article.id == "1"
    assert article.title == "Elvis Presley is alive and living in a cave"
    assert article.content == "A hobo wandering"
    assert article.external_url == "https://www.example.com/1"
    assert article.published_by == ["Hobo News"]
    assert article.date == datetime(2019, 11, 13, 13, 51, 47)
    assert article.reading_time == 3
    assert article.tags == ["cave", "elvis"]


@pytest.mark.parametrize(
    "published_by, expected_str",
    [
        (["Hobo News"], "Hobo News"),
        (["Hobo News", "Jack Black"], "Hobo News, Jack Black"),
        ([], ""),
        (None, ""),
    ],
)
def test_published_by_str(article, published_by, expected_str):
    article.published_by = published_by
    assert article.published_by_str() == expected_str


@pytest.mark.parametrize(
    "reading_time, expected_str",
    [
        (3, "3 minutes read"),
        (1, "1 minute read"),
        (None, ""),
    ],
)
def test_minutes_read(article, reading_time, expected_str):
    article.reading_time = reading_time
    assert article.minutes_read() == expected_str


def test_relative_date(article, monkeypatch):
    article.date = datetime(2019, 1, 1)

    monkeypatch.setattr(article, "_now", lambda: datetime(2019, 1, 2))
    assert article.relative_date() == "a day ago"


def test_relative_date_real_time(article):
    article.date = datetime(2019, 1, 1)
    assert "ago" in article.relative_date()
