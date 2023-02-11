"general tests for brutal_bag"
from unittest.mock import patch

from click.testing import CliRunner

from brutal_bag.cli import cli
from brutal_bag.cli import create_app
from brutal_bag.cli import Article

sample_articles = [
    Article(
        title="Elvis Presley is alive and living in a cave",
        id="1",
        content="A hobo wandering in the Appalachian mountains...",
    ),
    Article(
        title="A Yeti was seen on the New Jersey Turnpike",
        id="2",
        content="He wore Dock Martins... ",
    ),
]


def test_version():
    "test the version command"
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output.startswith("cli, version ")


@patch("brutal_bag.cli.create_app")
def test_serve(mock_create_app):
    "test the serve command"
    mock_app = mock_create_app.return_value
    runner = CliRunner()
    result = runner.invoke(cli, "serve")
    mock_app.run.assert_called_once()
    assert result.exit_code == 0


@patch("brutal_bag.cli.Article.get_all_unread")
def test_homepage(get_all_unread):
    "test the homepage"

    get_all_unread.return_value = sample_articles
    app = create_app()
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    html = response.data.decode()
    assert "<h1>BrutalBag</h1>" in html

    assert "Elvis Presley is alive and living in a cave" in html
    assert "/view/1" in html

    assert "A Yeti was seen on the New Jersey Turnpike" in html
    assert "/view/2" in html


@patch("brutal_bag.cli.Article.get_all_unread")
def test_view_article(get_all_unread):
    "test /view/<article_id>"
    get_all_unread.return_value = sample_articles

    app = create_app()
    client = app.test_client()
    response = client.get("/view/1")
    assert response.status_code == 200
    html = response.data.decode()

    assert "Elvis Presley is alive and living in a cave" in html
    assert "A hobo wandering" in html


@patch("brutal_bag.cli.Article.get_all_unread")
def test_view_article_not_found(get_all_unread):
    "test missing article on /view/<article_id>"

    get_all_unread.return_value = sample_articles
    app = create_app()
    client = app.test_client()
    response = client.get("/view/999")
    assert response.status_code == 404
    html = response.data.decode()

    assert "Not Found" in html
