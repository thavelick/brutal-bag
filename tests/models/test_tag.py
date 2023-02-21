import pytest

from brutal_bag.models.tag import Tag


@pytest.fixture(name="tag")
def tag_fixture():
    return Tag(
        id="1",
        label="Blogs",
        slug="blogs",
        unread_count=10,
    )


def test_create(tag):
    assert tag
    assert tag.id == "1"
    assert tag.label == "Blogs"
    assert tag.slug == "blogs"
    assert tag.unread_count == 10
