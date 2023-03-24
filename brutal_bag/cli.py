"""The command line interface for brutal_bag"""

import click
import quart.flask_patch

from quart import Quart, render_template, redirect
from werkzeug.exceptions import NotFound

from .models.favicon import get_favicon_url
from .models.wallabag import Wallabag
from .models.wallabag_article_fetcher import WallabagArticleFetcher
from .models.wallabag_article_updater import WallabagArticleUpdater
from .models.wallabag_tag_fetcher import WallabagTagFetcher


def create_app():
    "Create the flask app"
    app = Quart(__name__)

    wallabag = Wallabag()

    @app.context_processor
    async def count_unread():
        "Count the number of unread articles"

        count_unread = await WallabagArticleFetcher(wallabag).get_count(unread=True)
        return {
            "count_unread": count_unread,
        }

    @app.route("/")
    async def homepage():
        "Homepage"
        return await render_template(
            "articles.html",
            articles=await WallabagArticleFetcher(wallabag).get_all(unread=True),
        )

    @app.route("/history")
    async def history():
        "History"
        count_articles = await WallabagArticleFetcher(wallabag).get_count(unread=False)

        return await render_template(
            "articles.html",
            articles=await WallabagArticleFetcher(wallabag).get_all(unread=False),
            article_type="History",
            count_articles=count_articles,
        )

    @app.route("/favicon/<domain>")
    async def favicon(domain):
        url = f"https://{domain}"
        favicon_url = await get_favicon_url(url)
        if not favicon_url:
            favicon_url = "/static/favicon.ico"

        response = redirect(favicon_url)
        response.headers["Cache-Control"] = "public, max-age=604800"
        return response

    @app.route("/tags")
    async def tags():
        "List all tags"
        return await render_template(
            "tags.html", tags=await WallabagTagFetcher(wallabag).get_all()
        )

    @app.route("/tag/<tag_slug>/entries")
    async def tag_entries(tag_slug):
        "List all entries for a given tag"

        count_articles = await WallabagArticleFetcher(wallabag).get_count(
            unread=True, tag_name=tag_slug
        )

        return await render_template(
            "articles.html",
            articles=await WallabagArticleFetcher(wallabag).get_all(
                unread=True, tag_name=tag_slug
            ),
            article_type=tag_slug,
            count_articles=count_articles,
        )

    @app.route("/view/<article_id>")
    async def view_article(article_id):
        "View an article's content"
        article = await WallabagArticleFetcher(wallabag).get_by_id(article_id)
        if not article:
            raise NotFound
        await WallabagArticleUpdater(wallabag).update_read_state(article_id, True)
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
