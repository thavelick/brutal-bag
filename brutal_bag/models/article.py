"""Article model."""

from dataclasses import dataclass

from .wallabag import Wallabag


@dataclass
class Article:
    "An article from Wallabag"
    id: str
    content: str
    title: str

    external_url: str = None
    published_by: list = None

    def __post_init__(self):
        # make sure the id is a string
        self.id = str(self.id)

    @staticmethod
    def get_all_unread():
        "get all the unread articles from Wallabag."
        wallabag = Wallabag()
        article_data = wallabag.get_unread_articles()

        return [
            Article(
                **{
                    key: article.get(key)
                    for key in ["title", "id", "content", "published_by"]
                },
                external_url=article.get("url", None),
            )
            for article in article_data
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

    def published_by_str(self):
        "return a string of the publishers"
        if not self.published_by:
            return ""

        return ", ".join(self.published_by)
