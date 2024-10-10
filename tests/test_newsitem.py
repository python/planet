import configparser
import time
from pathlib import Path
from pprint import pprint

import feedparser
import planet
import pytest
from planet.cache import utf8

# Ensure the `tests/fixtures/` directory exists and feeds are stored there.
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture(name="channel_cache")
def channel_cache(rss_channel):
    try:
        yield rss_channel._cache
    finally:
        pprint(dict(rss_channel._cache))


@pytest.fixture(scope="module", name="rss_feed")
def load_rss_feed():
    """Load and parse the sample RSS feed fixture."""
    with open(FIXTURES_DIR / "sample_rss.xml", encoding="utf-8") as rss_file:
        feed_data = rss_file.read()
    return feedparser.parse(feed_data)


@pytest.fixture(scope="module", name="atom_feed")
def load_atom_feed():
    """Load and parse the sample Atom feed fixture."""
    with open(FIXTURES_DIR / "sample_atom.xml", encoding="utf-8") as atom_file:
        feed_data = atom_file.read()
    return feedparser.parse(feed_data)


def test_newsitem_from_rss(rss_feed, rss_channel):
    """Test that we can create a NewsItem from an RSS feed item."""
    item = rss_feed.entries[0]
    newsitem = planet.NewsItem(rss_channel, rss_feed.entries[0]["id"])
    newsitem.update(item)
    assert newsitem.title == "Example Item 1"
    assert newsitem.link == "https://example.com/item1"
    assert newsitem.date[0] == 2021
    assert newsitem.author == "author@example.com (John Doe)"
    assert newsitem.content == "This is a description of item 1"
    assert newsitem.summary == "This is a description of item 1"


def test_newsitem_from_atom(atom_feed, atom_channel):
    """Test that we can create a NewsItem from an RSS feed item."""
    item = atom_feed.entries[0]
    newsitem = planet.NewsItem(atom_channel, atom_feed.entries[0]["id"])
    newsitem.update(item)
    assert newsitem.title == "Example Entry 1"
    assert newsitem.link == "https://example.com/entry1"
    # parse the iso timestamp into a time tuple
    assert newsitem.date[0] == 2021
    assert newsitem.content == "This is a summary of entry 1"
    assert newsitem.summary == "This is a summary of entry 1"


def test_caching_newsitem(rss_feed, rss_channel):
    """Test that we can create a NewsItem from an RSS feed item."""
    item = rss_feed.entries[0]
    newsitem = planet.NewsItem(rss_channel, rss_feed.entries[0]["id"])
    newsitem.update(item)
    newsitem.cache_write()

    # now try read the newsitem, but with the cache; we should be able to
    # get the values before updating
    newsitem = planet.NewsItem(rss_channel, rss_feed.entries[0]["id"])
    assert newsitem.title == "Example Item 1"
    assert newsitem.link == "https://example.com/item1"
    assert newsitem.date[0] == 2021
    assert newsitem.author == "author@example.com (John Doe)"
    assert newsitem.content == "This is a description of item 1"
    assert newsitem.summary == "This is a description of item 1"


# These tests are aimed at testing the specifications of the cache; we are looking at key structures
# and internals, so that we can have some sense of implementation consistency.


@pytest.fixture(name="news_item")
def news_item(
    rss_channel,
    rss_feed,
):
    return planet.NewsItem(rss_channel, rss_feed.entries[0]["id"])


@pytest.fixture(name="sample_entry")
def sample_entry(rss_feed):
    return rss_feed.entries[0]


def test_cache_write_and_read(news_item, sample_entry, channel_cache):
    # First, update the news item using the sample_entry
    news_item.update(sample_entry)
    news_item.cache_write(sync=True)

    # Now, inspect the cache to see if keys have been stored correctly
    assert f"{news_item.id} title" in channel_cache
    assert f"{news_item.id} link" in channel_cache
    assert channel_cache[f"{news_item.id} title"] == utf8(sample_entry["title"])
    assert channel_cache[f"{news_item.id} link"] == utf8(sample_entry["link"])

    # Date value stored as a string representation of the time tuple
    assert f"{news_item.id} updated" in channel_cache
    assert channel_cache[f"{news_item.id} updated"] == " ".join(
        map(str, sample_entry["updated_parsed"])
    )


def test_cache_clear(news_item, sample_entry, channel_cache):
    # Update and save to cache
    news_item.update(sample_entry)
    news_item.cache_write(sync=True)

    # Ensure keys are there
    assert f"{news_item.id} title" in channel_cache

    # Now clear the cache for the news_item
    news_item.cache_clear(sync=True)

    # Ensure keys are removed from the cache
    assert f"{news_item.id} title" not in channel_cache
    assert f"{news_item.id} link" not in channel_cache
    assert f"{news_item.id} updated" not in channel_cache


def test_cache_key_type(news_item, sample_entry, channel_cache):
    # Update and save to cache
    news_item.update(sample_entry)
    news_item.cache_write(sync=True)

    # Ensure keys and types are correct
    assert channel_cache[f"{news_item.id} title"] == "Example Item 1"
    assert channel_cache[f"{news_item.id} title type"] == "string"
    assert channel_cache[f"{news_item.id} updated type"] == "date"


def test_cache_reload(news_item, sample_entry, rss_channel):
    # Update and save to cache
    news_item.update(sample_entry)
    news_item.cache_write(sync=True)

    # Create a new NewsItem instance with the same cache, and reload
    new_item = planet.NewsItem(rss_channel, f"{news_item.id}")
    new_item.cache_read()

    # Check that the data is retrieved as expected
    assert new_item.get("title") == "Example Item 1"
    assert new_item.get("link") == "https://example.com/item1"
    assert new_item.get("date") == sample_entry["date_parsed"]


def test_cache_date_field(news_item, sample_entry, rss_channel, channel_cache):
    # Ensure the date field gets cached properly
    news_item.update(sample_entry)
    news_item.cache_write(sync=True)

    # Check that the date type is correctly saved as dates
    assert f"{news_item.id} updated" in channel_cache
    assert f"{news_item.id} updated type" in channel_cache
    assert channel_cache[f"{news_item.id} updated type"] == "date"

    # Reload item and ensure the date value is parsed correctly
    new_item = planet.NewsItem(rss_channel, f"{news_item.id}")
    new_item.cache_read()

    # Verify that the date field is properly restored as date tuple
    assert new_item.get("date") == sample_entry["date_parsed"]


def test_delete_key_from_cache(news_item, sample_entry, channel_cache):
    # Update and save to cache
    news_item.update(sample_entry)
    news_item.cache_write(sync=True)

    # Delete 'title' key using NewsItem's del_key method
    news_item.del_key("title")
    news_item.cache_write(sync=True)

    # Ensure 'title' key is deleted from cache
    assert f"{news_item.id} title" not in channel_cache
