"""Article model."""

from dataclasses import dataclass
from datetime import datetime, timedelta
import humanize


from .wallabag import Wallabag


@dataclass
class Article:
    "An article from a reader or bookmarking service like Wallabag"
    id: str
    content: str
    title: str

    external_url: str = None
    published_by: list = None
    date: datetime = None
    reading_time: int = None
    tags: list = None

    @staticmethod
    def from_wallabag_dict(source_dict):
        "Create an Article from a wallabag response dict."
        dest_dict = {
            key: source_dict.get(key)
            for key in [
                "content",
                "published_by",
                "reading_time",
                "title",
            ]
        }

        dest_dict["id"] = str(source_dict.get("id"))
        dest_dict["external_url"] = source_dict.get("url")
        dest_dict["tags"] = source_dict.get("tags", [])

        # should probably refactor all this at some point to save
        # both published_at and created_at in the Article model,
        # then just render the right one in the template
        article_date = source_dict.get("published_at") or source_dict.get("created_at")

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

    def published_by_str(self):
        "return a string of the publishers"
        if not self.published_by:
            return ""

        return ", ".join(self.published_by)

    def relative_date(self):
        "return a humanized relative date"
        if not self.date:
            return ""

        return humanize.naturaltime(self._now() - self.date)

    def minutes_read(self):
        "return the number of minutes to read the article"

        # reading time contains the number of minutes it will take to read
        # the article. This function will return a string like "5 minutes read"
        # or "1 minute read".
        if not self.reading_time:
            return ""

        if self.reading_time == 1:
            return "1 minute read"

        return f"{self.reading_time} minutes read"

    def _now(self):
        "return the current date"
        return datetime.utcnow()
