"""The command line interface for brutal_bag"""
from flask import Flask, render_template

import click


def create_app():
    "Create the flask app"
    app = Flask(__name__)

    @app.route("/")
    def homepage():
        "Homepage"
        return render_template("index.html")

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
