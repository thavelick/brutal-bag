import os
import time
from wallabagapi import WallabagAPI


class MissingEnvironment(Exception):
    pass


class Wallabag:
    def __init__(self):
        environment = self.get_environment()
        self.client_id = environment.get("WALLABAG_CLIENT_ID")
        self.client_secret = environment.get("WALLABAG_CLIENT_SECRET")
        self.password = environment.get("WALLABAG_PASSWORD")
        self.url = environment.get("WALLABAG_URL")
        self.username = environment.get("WALLABAG_USERNAME")

        self.wallabag_api = None
        self.token = None
        self.token_expires_at = None

    def get_environment(self):
        return os.environ

    def check_environment(self):
        for required_env in [
            "WALLABAG_CLIENT_ID",
            "WALLABAG_CLIENT_SECRET",
            "WALLABAG_PASSWORD",
            "WALLABAG_URL",
            "WALLABAG_USERNAME",
        ]:
            if required_env not in self.get_environment():
                raise MissingEnvironment(
                    f"Missing required environment variable {required_env}"
                )

    async def connect(self):
        self.check_environment()

        if self.token and self.token_expires_at > time.time():
            return

        self.token = await WallabagAPI.get_token(
            host=self.url,
            username=self.username,
            password=self.password,
            client_id=self.client_id,
            client_secret=self.client_secret,
        )

        self.wallabag_api = WallabagAPI(
            host=self.url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=self.token,
            extension="json",
        )

        self.token_expires_at = time.time() + 3600

    async def get_unread_articles(self):
        await self.connect()
        response = await self.wallabag_api.get_entries(archive=0)
        articles = response["_embedded"]["items"]
        return articles

    async def get_unread_articles_by_tag(self, tag):
        await self.connect()
        response = await self.wallabag_api.get_entries(archive=0, tags=[tag])
        articles = response["_embedded"]["items"]
        return articles

    async def get_article_by_id(self, article_id):
        await self.connect()
        article = await self.wallabag_api.get_entry(article_id)
        return article

    async def get_all_tags(self):
        await self.connect()
        tags = await self.wallabag_api.get_tags()
        return tags

    async def get_article_count(self, unread=True, tag=None):
        "get the number of articles in Wallabag for given parameters."
        await self.connect()
        parameters = {
            "archive": 0 if unread else 1,
            "perPage": 1,
        }
        if tag:
            parameters["tags"] = [tag]

        response = await self.wallabag_api.get_entries(**parameters)
        return response["total"]
