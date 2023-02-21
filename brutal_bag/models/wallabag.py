import os

import httpx
import json
import time


class MissingEnvironment(Exception):
    pass


class Wallabag:
    """A Wallabag client"""

    def __init__(self):
        self.client_id = os.environ.get("WALLABAG_CLIENT_ID")
        self.client_secret = os.environ.get("WALLABAG_CLIENT_SECRET")
        self.password = os.environ.get("WALLABAG_PASSWORD")
        self.url = os.environ.get("WALLABAG_URL")
        self.username = os.environ.get("WALLABAG_USERNAME")

    def get_oauth_token(self):
        """
        Get the oauth token for a wallabag server.

        try to load the token from the file system. If the token is expired,
        get a new one from the api and save that to the file system.
        Returns:
            The oauth token.
        """
        token_data = {"expiration": 0}
        token_cache_file = "/tmp/wallabag_token.json"

        # load data from the cache file if it exists
        if os.path.exists(token_cache_file):
            with open(token_cache_file, "r", encoding="utf-8") as token_file:
                token_data = json.load(token_file)

        if token_data["expiration"] < int(round(time.time())):
            token_data = self.get_oauth_token_and_expiration_from_api()
            with open(token_cache_file, "w", encoding="utf-8") as token_file:
                json.dump(token_data, token_file)
        return str(token_data["token"])

    def get_oauth_token_and_expiration_from_api(self):
        """
        Call out to the api to get an oauth token for future requests.
        Args:
            wallabag_url: The url of the wallabag server to get the token for.
        Returns:
            A dict containing the token and expiration as a unix timestamp.
        """
        # make sure we have all the required environment variables
        if not all(
            [self.client_id, self.client_secret, self.password, self.url, self.username]
        ):
            raise MissingEnvironment("Missing required environment variables")

        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": self.password,
        }

        response_data = httpx.post(f"{self.url}/oauth/v2/token", data=data).json()

        current_unix_timestamp = int(round(time.time()))
        expiration_timestamp = current_unix_timestamp + response_data["expires_in"]
        return {
            "token": response_data["access_token"],
            "expiration": expiration_timestamp,
        }

    def get_unread_articles(self):
        """
        Get all the unread articles from Wallabag.
        Returns:
            A list of dicts containing the article data.
        """

        token = self.get_oauth_token()

        response = httpx.get(
            f"{self.url}/api/entries.json",
            headers={"Authorization": f"Bearer {token}"},
            params={"archive": 0, "starred": 0, "limit": 1},
        )

        return response.json().get("_embedded", {}).get("items", [])
