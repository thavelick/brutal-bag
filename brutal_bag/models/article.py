"""Article model."""

from dataclasses import dataclass

from brutal_bag.models.wallabag import Wallabag


@dataclass
class Article:
    "An article from Wallabag"
    title: str
    id: str
    content: str

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
                title=article["title"],
                id=article["id"],
                content=article["content"],
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
