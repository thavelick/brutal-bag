class WallabagArticleUpdater:
    def __init__(self, wallabag):
        self.wallabag = wallabag

    async def update_read_state(self, article_id, is_read):
        """Update the read state of an article."""
        return await self.wallabag.set_article_read(article_id, is_read)

    async def update_starred_state(self, article_id, is_starred):
        """Update the starred state of an article."""
        return await self.wallabag.set_article_starred(article_id, is_starred)
