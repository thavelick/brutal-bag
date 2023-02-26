import asyncio

from .tag import Tag


class WallabagTagFetcher:
    def __init__(self, wallabag):
        self.wallabag = wallabag

    async def get_all(self):
        "get all the tags, with counts, from Wallabag."
        tag_dicts = await self.wallabag.get_all_tags()
        tags = [Tag(**tag_dict) for tag_dict in tag_dicts]
        tags.sort(key=lambda tag: tag.label)

        tasks = [
            self.wallabag.get_article_count(unread=True, tag=tag.label) for tag in tags
        ]
        for i, task in enumerate(asyncio.as_completed(tasks)):
            tags[i].unread_count = await task

        return tags
