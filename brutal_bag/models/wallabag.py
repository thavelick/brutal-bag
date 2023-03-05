import os
import time
from wallabagapi import WallabagAPI


class MissingEnvironment(Exception):
    pass


class WallabagResultList(list):
    def __init__(self, items, total):
        super().__init__(items)
        self.total = total


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

    async def get_articles(self, unread=True, tag=None, per_page=30):
        await self.connect()
        parameters = {
            "archive": 0 if unread else 1,
            "perPage": per_page,
        }
        if tag:
            parameters["tags"] = [tag]

        response = await self.wallabag_api.get_entries(**parameters)
        return WallabagResultList(response["_embedded"]["items"], response["total"])

    async def get_article_by_id(self, article_id):
        await self.connect()
        return await self.wallabag_api.get_entry(article_id)

    async def get_all_tags(self):
        await self.connect()
        return await self.wallabag_api.get_tags()

    async def get_article_count(self, unread=True, tag=None):
        "get the number of articles in Wallabag for given parameters."
        result_list = await self.get_articles(unread=unread, tag=tag, per_page=1)
        return result_list.total
