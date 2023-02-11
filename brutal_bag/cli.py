"""The command line interface for brutal_bag"""
import os
from dataclasses import dataclass

import click
import httpx
import json
import time
from flask import Flask, render_template
from werkzeug.exceptions import NotFound


class Wallabag:
    """A Wallabag client"""

    def __init__(self):
        self.client_id = os.environ["WALLABAG_CLIENT_ID"]
        self.client_secret = os.environ["WALLABAG_CLIENT_SECRET"]
        self.password = os.environ["WALLABAG_PASSWORD"]
        self.url = os.environ["WALLABAG_URL"]
        self.username = os.environ["WALLABAG_USERNAME"]

    def get_oauth_token(self):
        """
        Get the oauth token for a wallabag server.

        try to load the token from the file system. If the token is expired,
        get a new one from the api and save that to the file system.
        Returns:
            The oauth token.
        """
        token_data = {"expiration": 0}
        token_cache_file = "/tmp/wallabag_token.json"

        # load data from the cache file if it exists
        if os.path.exists(token_cache_file):
            with open(token_cache_file, "r", encoding="utf-8") as token_file:
                token_data = json.load(token_file)

        if token_data["expiration"] < int(round(time.time())):
            token_data = self.get_oauth_token_and_expiration_from_api()
            with open(token_cache_file, "w", encoding="utf-8") as token_file:
                json.dump(token_data, token_file)
        return str(token_data["token"])

    def get_oauth_token_and_expiration_from_api(self):
        """
        Call out to the api to get an oauth token for future requests.
        Args:
            wallabag_url: The url of the wallabag server to get the token for.
        Returns:
            A dict containing the token and expiration as a unix timestamp.
        """
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
        }

        response_data = httpx.post(f"{self.url}/oauth/v2/token", data=data).json()

        current_unix_timestamp = int(round(time.time()))
        expiration_timestamp = current_unix_timestamp + response_data["expires_in"]
        return {
            "token": response_data["access_token"],
            "expiration": expiration_timestamp,
        }

    def get_unread_articles(self):
        """
        Get all the unread articles from Wallabag.
        Returns:
            A list of dicts containing the article data.
        """

        token = self.get_oauth_token()

        response = httpx.get(
            f"{self.url}/api/entries.json",
            headers={"Authorization": f"Bearer {token}"},
            params={"archive": 0, "starred": 0, "limit": 1},
        )

        return response.json().get("_embedded", {}).get("items", [])


@dataclass
class Article:
    "An article from Wallabag"
    title: str
    id: str
    content: str

    @staticmethod
    def get_all_unread():
        "get all the unread articles from Wallabag."
        wallabag = Wallabag()
        article_data = wallabag.get_unread_articles()
        return [Article(**article) for article in article_data]

    @classmethod
    def get_by_id(cls, article_id):
        """
        get an article by it's id.

        Return None if it doesn't exist.
        """

        articles_found = [
            article for article in cls.get_all_unread() if article.id == article_id
        ]
        if len(articles_found) == 1:
            return articles_found[0]
        return None


def create_app():
    "Create the flask app"
    app = Flask(__name__)

    @app.route("/")
    def homepage():
        "Homepage"
        return render_template("index.html", articles=Article.get_all_unread())

    @app.route("/view/<article_id>")
    def view_article(article_id):
        "View an article's content"
        article = Article.get_by_id(article_id)

        if not article:
            raise NotFound

        return render_template("view.html", article=article)

    return app


@click.group()
@click.version_option()
def cli():
    "A js-optional frontend for Wallabag"


@cli.command(name="serve")
@click.option("-d", "--debug", default=False, help="run in debug mode")
def serve(debug):
    "Start the web server"
    app = create_app()
    app.debug = debug
    print("debug mode", debug)
    app.run()
