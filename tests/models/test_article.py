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
        is_read=False,
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
    assert article.is_read is False
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


@pytest.mark.parametrize(
    "external_url, expected_domain",
    [
        ("https://www.example.com/test-article", "www.example.com"),
        (None, ""),
        ("", ""),
        ("invalid_url", ""),
    ],
)
def test_external_domain(article, external_url, expected_domain):
    article.external_url = external_url
    assert article.external_domain() == expected_domain


def test_read_string_read(article):
    article.is_read = True
    assert article.read_string() == "Read"


def test_read_string_unread(article):
    article.is_read = False
    assert article.read_string() == "Unread"


def test_read_string_read_inverse(article):
    article.is_read = True
    assert article.read_string(show_inverse=True) == "Unread"


def test_read_string_unread_inverse(article):
    article.is_read = False
    assert article.read_string(show_inverse=True) == "Read"
