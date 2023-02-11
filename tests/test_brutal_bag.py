"general tests for brutal_bag"
from unittest.mock import patch

from click.testing import CliRunner

from brutal_bag.cli import cli
from brutal_bag.cli import create_app


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


def test_homepage():
    "test the homepage"
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
