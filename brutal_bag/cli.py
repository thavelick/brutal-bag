"""The command line interface for brutal_bag"""
from flask import Flask

import click


def create_app():
    "Create the flask app"
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        "Just print hello world for now"
        return "<p>Hello, World!</p>"

    return app


@click.group()
@click.version_option()
def cli():
    "A js-optional frontend for Wallabag"


@cli.command(name="serve")
def serve():
    "Start the web server"
    app = create_app()
    app.run()
