"general tests for brutal_bag"

from click.testing import CliRunner
import pytest


from brutal_bag.cli import cli
from brutal_bag.cli import create_app
from brutal_bag.models.article import Article
from brutal_bag.models.tag import Tag
from brutal_bag.models.wallabag_article_fetcher import WallabagArticleFetcher
from brutal_bag.models.wallabag_tag_fetcher import WallabagTagFetcher

sample_articles = [
    Article(
        title="Elvis Presley is alive and living in a cave",
        id="1",
        content="A hobo wandering in the Appalachian mountains...",
        external_url="https://www.elvispresley.com/article/1",
        tags=[],
    ),
    Article(
        title="A Yeti was seen on the New Jersey Turnpike",
        id="2",
        content="He wore Dock Martins... ",
        published_by=["Questionable Geographic"],
        external_url="https://www.questionablegeographic.com/news/45687",
        tags=[],
    ),
]


@pytest.fixture(name="client")
def client_fixture():
    app = create_app()
    return app.test_client()


def test_version():
    "test the version command"
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output.startswith("cli, version ")


def test_serve(mocker):
    "test the serve command"
    mock_create_app = mocker.patch("brutal_bag.cli.create_app")
    mock_app = mock_create_app.return_value
    runner = CliRunner()
    result = runner.invoke(cli, "serve")
    mock_app.run.assert_called_once()
    assert result.exit_code == 0


async def test_homepage(mocker, client):
    "test the homepage"

    mocker.patch.object(
        WallabagArticleFetcher, "get_all_unread", return_value=sample_articles
    )
    mocker.patch.object(
        WallabagArticleFetcher, "get_count", return_value=len(sample_articles)
    )
    response = await client.get("/")

    assert response.status_code == 200
    html = (await response.data).decode()
    assert "Brutal<span>Bag</span>" in html

    assert "Elvis Presley is alive and living in a cave" in html
    assert "/view/1" in html

    assert "A Yeti was seen on the New Jersey Turnpike" in html
    assert "Questionable Geographic" in html
    assert "/view/2" in html


async def test_view_article(mocker, client):
    "test /view/<article_id>"
    mocker.patch.object(
        WallabagArticleFetcher, "get_all_unread", return_value=sample_articles
    )
    mocker.patch.object(
        WallabagArticleFetcher, "get_count", return_value=len(sample_articles)
    )

    response = await client.get("/view/1")
    assert response.status_code == 200
    html = (await response.data).decode()

    assert "Elvis Presley is alive and living in a cave" in html
    assert "A hobo wandering" in html


async def test_view_article_not_found(mocker, client):
    "test missing article on /view/<article_id>"
    mocker.patch.object(
        WallabagArticleFetcher, "get_all_unread", return_value=sample_articles
    )

    response = await client.get("/view/999")
    assert response.status_code == 404
    html = (await response.data).decode()

    assert "Not Found" in html


async def test_tags(mocker, client):
    "test /tags"
    mocker.patch.object(
        WallabagTagFetcher,
        "get_all",
        return_value=[Tag(id="1", label="Blogs", slug="blogs", unread_count=555)],
    )
    mocker.patch.object(WallabagArticleFetcher, "get_count", return_value=222)

    response = await client.get("/tags")
    assert response.status_code == 200
    html = (await response.data).decode()

    assert "Blogs" in html
    assert "222" in html
    assert "555" in html


@pytest.mark.parametrize(
    "favicon_url, expected_location",
    [
        ("https://example.com/favicon.png", "https://example.com/favicon.png"),
        (None, "/static/favicon.ico"),
    ],
)
async def test_favicon_async(client, mocker, favicon_url, expected_location):
    mocker.patch(
        "brutal_bag.cli.get_favicon_url",
        return_value=favicon_url,
    )

    response = await client.get("/favicon/example.com")

    assert response.status_code == 302
    assert response.headers["Location"] == expected_location
    assert "Cache-Control" in response.headers
    assert response.headers["Cache-Control"] == "public, max-age=604800"
