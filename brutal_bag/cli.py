"""The command line interface for brutal_bag"""
import asyncio


import click
import quart.flask_patch

from quart import Quart, render_template, redirect
from werkzeug.exceptions import NotFound
from flask_caching import Cache

from .models.favicon import get_favicon_url
from .models.wallabag import Wallabag
from .models.wallabag_async import WallabagAsync
from .models.wallabag_article_fetcher import WallabagArticleFetcher
from .models.wallabag_tag_fetcher import WallabagTagFetcher


def create_app():
    "Create the flask app"
    app = Quart(__name__)
    app.config["CACHE_TYPE"] = "SimpleCache"
    cache = Cache(app)
    wallabag = Wallabag()

    wallabag_async = WallabagAsync()

    @cache.cached(timeout=60)
    async def get_all_unread():
        return await WallabagArticleFetcher(wallabag_async).get_all_unread()

    @app.context_processor
    def count_unread():
        "Count the number of unread articles"

        return {"count_unread": len(get_all_unread())}

    @app.route("/")
    async def homepage():
        "Homepage"
        return await render_template("index.html", articles=get_all_unread())

    @app.route("/favicon/<domain>")
    async def favicon(domain):
        url = f"https://{domain}"
        favicon_url = get_favicon_url(url)
        if not favicon_url:
            favicon_url = "/static/favicon.ico"

        response = redirect(favicon_url)
        response.headers["Cache-Control"] = "public, max-age=604800"
        return response

    @app.route("/tags")
    async def tags():
        "List all tags"
        return await render_template(
            "tags.html", tags=await WallabagTagFetcher(wallabag_async).get_all()
        )

    @app.route("/view/<article_id>")
    async def view_article(article_id):
        "View an article's content"
        article = await WallabagArticleFetcher(wallabag_async).get_by_id(article_id)

        if not article:
            raise NotFound

        return await render_template("view.html", article=article)

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
