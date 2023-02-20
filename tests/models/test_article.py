from datetime import datetime

from brutal_bag.models.article import Article


def make_article():
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


def test_create():
    article = make_article()

    assert article
    assert article.id == "1"
    assert article.title == "Elvis Presley is alive and living in a cave"
    assert article.content == "A hobo wandering"
    assert article.external_url == "https://www.example.com/1"
    assert article.published_by == ["Hobo News"]
    assert article.date == datetime(2019, 11, 13, 13, 51, 47)
    assert article.reading_time == 3
    assert article.tags == ["cave", "elvis"]


def test_from_wallabag_dict():
    source_dict = {
        "id": 1,
        "title": "Elvis Presley is alive and living in a cave",
        "content": "A hobo wandering",
        "url": "https://www.example.com/1",
        "published_by": ["Hobo News"],
        "published_at": "2019-11-13T13:51:47-0700",
        "reading_time": 3,
        "tags": ["cave", "elvis"],
    }

    article = Article.from_wallabag_dict(source_dict)

    assert article
    assert article.id == "1"
    assert article.title == "Elvis Presley is alive and living in a cave"
    assert article.content == "A hobo wandering"
    assert article.external_url == "https://www.example.com/1"
    assert article.published_by == ["Hobo News"]
    assert article.date == datetime(2019, 11, 13, 20, 51, 47)
    assert article.reading_time == 3
    assert article.tags == ["cave", "elvis"]


# TODO: Make this data-driven
def test_published_by_str():
    article = make_article()

    article.published_by = ["Hobo News"]
    assert article.published_by_str() == "Hobo News"

    article.published_by = ["Hobo News", "Jack Black"]
    assert article.published_by_str() == "Hobo News, Jack Black"

    article.published_by = []
    assert article.published_by_str() == ""

    article.published_by = None
    assert article.published_by_str() == ""


def test_minutes_read():
    article = make_article()

    article.reading_time = 3
    assert article.minutes_read() == "3 minutes read"

    article.reading_time = 1
    assert article.minutes_read() == "1 minute read"

    article.reading_time = None
    assert article.minutes_read() == ""


def test_relative_date(monkeypatch):
    article = make_article()
    article.date = datetime(2019, 1, 1)

    monkeypatch.setattr(article, "_now", lambda: datetime(2019, 1, 2))
    assert article.relative_date() == "a day ago"
