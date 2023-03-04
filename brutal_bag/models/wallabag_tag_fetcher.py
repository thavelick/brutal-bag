import asyncio

from .tag import Tag


class WallabagTagFetcher:
    def __init__(self, wallabag):
        self.wallabag = wallabag

    async def get_all(self):
        "get all the tags, with counts, from Wallabag."

        async def tag_from_dict(tag_dict):
            tag = Tag(**tag_dict)
            tag.unread_count = await self.wallabag.get_article_count(
                unread=True, tag=tag.label
            )
            return tag

        tag_dicts = await self.wallabag.get_all_tags()

        tasks = [tag_from_dict(tag_dict) for tag_dict in tag_dicts]
        tags = await asyncio.gather(*tasks)

        return tags
