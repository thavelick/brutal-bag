from .tag import Tag
from .wallabag_article_fetcher import WallabagArticleFetcher


class WallabagTagFetcher:
    def __init__(self, wallabag):
        self.wallabag = wallabag

    async def get_all(self):
        "get all the tags from Wallabag."
        tag_data = await self.wallabag.get_all_tags()

        all_unread_articles = await WallabagArticleFetcher(
            self.wallabag
        ).get_all_unread()
        tags = []
        for tag_dict in tag_data:
            tag_dict["unread_count"] = len(
                [
                    article
                    for article in all_unread_articles
                    if tag_dict["label"] in [tag.label for tag in article.tags]
                ]
            )
            tags.append(Tag(**tag_dict))

        return tags
