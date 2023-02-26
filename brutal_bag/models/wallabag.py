import json
import os
import time
from wallabagapi import WallabagAPI


class MissingEnvironment(Exception):
    pass


class Wallabag:
    def __init__(self):
        for required_env in [
            "WALLABAG_CLIENT_ID",
            "WALLABAG_CLIENT_SECRET",
            "WALLABAG_PASSWORD",
            "WALLABAG_URL",
            "WALLABAG_USERNAME",
        ]:
            if required_env not in os.environ:
                raise MissingEnvironment(
                    f"Missing required environment variable {required_env}"
                )

        self.client_id = os.environ["WALLABAG_CLIENT_ID"]
        self.client_secret = os.environ["WALLABAG_CLIENT_SECRET"]
        self.password = os.environ["WALLABAG_PASSWORD"]
        self.url = os.environ["WALLABAG_URL"]
        self.username = os.environ["WALLABAG_USERNAME"]
        self.wallabag = None
        self.token = None
        self.token_expires_at = None

    async def connect(self):
        if self.token and self.token_expires_at > time.time():
            return

        self.token = await WallabagAPI.get_token(
            host=self.url,
            username=self.username,
            password=self.password,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

        self.wallabag = WallabagAPI(
            host=self.url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=self.token,
            extension="json",
        )

        self.token_expires_at = time.time() + 3600

    async def get_unread_articles(self):
        await self.connect()
        response = await self.wallabag.get_entries(archive=0)
        articles = response["_embedded"]["items"]
        return articles

    async def get_all_tags(self):
        await self.connect()
        tags = await self.wallabag.get_tags()
        return tags
