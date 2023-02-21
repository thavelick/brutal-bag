"""Article model."""

from dataclasses import dataclass
from datetime import datetime, timedelta
import humanize


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
