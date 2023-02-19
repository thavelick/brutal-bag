"""The command line interface for brutal_bag"""
import click
from flask import Flask, render_template
from werkzeug.exceptions import NotFound

from .models.article import Article


def create_app():
    "Create the flask app"
    app = Flask(__name__)

    @app.context_processor
    def count_unread():
        "Count the number of unread articles"
        return {"count_unread": len(Article.get_all_unread())}

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
