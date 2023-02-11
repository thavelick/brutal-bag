"""The command line interface for brutal_bag"""
# import dataclasses
from dataclasses import dataclass

import click
from flask import Flask, render_template
from werkzeug.exceptions import NotFound


# Make a dataclass for articles


@dataclass
class Article:
    "An article from Wallabag"
    title: str
    id: str
    content: str

    @staticmethod
    def get_all_unread():
        "get all the unread articles"
        return [
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
