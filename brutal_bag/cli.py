"""The command line interface for brutal_bag"""
from dataclasses import dataclass

import click
from flask import Flask, render_template
from werkzeug.exceptions import NotFound
from .models.wallabag import Wallabag


@dataclass
class Article:
    "An article from Wallabag"
    title: str
    id: str
    content: str

    def __post_init__(self):
        # make sure the id is a string
        self.id = str(self.id)

    @staticmethod
    def get_all_unread():
        "get all the unread articles from Wallabag."
        wallabag = Wallabag()
        article_data = wallabag.get_unread_articles()
        return [
            Article(
                title=article["title"],
                id=article["id"],
                content=article["content"],
            )
            for article in article_data
        ]

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
