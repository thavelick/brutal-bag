from datetime import datetime, timedelta


from .article import Article
from .tag import Tag


class WallabagArticleFetcher:
    def __init__(self, wallabag):
        self.wallabag = wallabag

    @staticmethod
    def wallabag_entry_to_article(entry):
        dest_dict = {
            key: entry.get(key)
            for key in [
                "content",
                "published_by",
                "reading_time",
                "title",
            ]
        }

        dest_dict["id"] = str(entry.get("id"))
        dest_dict["external_url"] = entry.get("url")

        raw_tags = entry.get("tags", [])

        dest_dict["tags"] = [Tag(**tag) for tag in raw_tags]

        # should probably refactor all this at some point to save
        # both published_at and created_at in the Article model,
        # then just render the right one in the template
        article_date = entry.get("published_at") or entry.get("created_at")

        if article_date:
            # article_date looks like 2019-11-13T13:51:47-0700
            # let's parse that to a datetime without a time zone
            time_zone_part = article_date[-5:]
            date = datetime.strptime(article_date[:-5], "%Y-%m-%dT%H:%M:%S")
            date = date - timedelta(
                hours=int(time_zone_part[:3]), minutes=int(time_zone_part[3:])
            )

            dest_dict["date"] = date

        return Article(**dest_dict)

    async def get_all_unread(self):
        "get all the unread articles from Wallabag."
        article_data = await self.wallabag.get_unread_articles()
        return [self.wallabag_entry_to_article(article) for article in article_data]

    async def get_by_id(self, article_id):
        """
        get an article by it's id.

        Return None if it doesn't exist.
        """
        articles_found = [
            article
            for article in await self.get_all_unread()
            if article.id == article_id
        ]
        if len(articles_found) == 1:
            return articles_found[0]
        return None
