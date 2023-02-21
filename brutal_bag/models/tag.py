"""Tag model."""

from dataclasses import dataclass


@dataclass
class Tag:
    "A tag or category for an article"
    id: str
    label: str
    slug: str
    unread_count: int = 0
