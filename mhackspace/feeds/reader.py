import lxml
import feedparser
from io import StringIO
from lxml.html.clean import Cleaner

from django.utils.html import escape


namespaces = {}
urls = [
    "https://feeds.feedburner.com/projects-jl",
    "https://hackaday.com/tag/emf-camp-2018/feed/",
    "https://maidstone-hackspace.org.uk/blog/rss/",
    "http://webboggles.com/feed/",
    "https://blog.digitaloctave.com/rss.xml",
]
html_parser = lxml.etree.HTMLParser()


def parse_content(content):
    html_img_cleaner = Cleaner(allow_tags=["img"], remove_unknown_tags=False)
    html_img_cleaner.allow_tags = ["img"]

    xml_parser = lxml.etree.XMLParser(
        remove_blank_text=True, ns_clean=True, encoding="utf-8"
    )

    return lxml.etree.XML("<div>" + escape(content) + "</div>", xml_parser)


def fetch_image_from_node_text(text):
    description = lxml.etree.parse(StringIO(text), html_parser)
    for image in description.xpath(".//img"):
        return image.get("src")
    return None


def fetch_node_text(node, name, default=u""):
    """fetch the text from the node we are given, we are working in unicode
        so decode byte strings to unicode"""
    result = node.xpath("./%s" % name)
    if result is None or len(result) is 0:
        return default

    if type(result[-1].text) is str:
        return result[-1].text.encode("utf-8")
    else:
        return result[-1].text


def fetch_image(post, node, namespaces):
    """Try and get an image from an item in the feed, use various fall back methods"""
    if hasattr(post, "media_thumbnail"):
        image = post.media_thumbnail
        if image:
            return image[0].get("url")

    if hasattr(post, "content"):
        content = " ".join(c.value for c in post.content)
        image = fetch_image_from_node_text(content)
        if image:
            return image

    # final attempt at getting an image from the item using description
    result = fetch_node_text(node, "description")
    if result:
        image = fetch_image_from_node_text(result)
        if image:
            return image

    # no image so lets fall back to the channel image if it exists
    return None


def fetch_feeds(feeds):
    articles = []

    for feed in feeds:
        url = feed.get("url")
        parsed = feedparser.parse(url)
        namespaces = {}
        if hasattr(parsed, "namespaces"):
            namespaces = parsed.namespaces
        feed_image = ""
        if hasattr(parsed.feed, "image"):
            feed_image = parsed.feed.image.get("href")
        for post in parsed.entries:
            root_node = parse_content(post.description)
            image = fetch_image(post, root_node, namespaces) or feed_image
            yield {
                "url": post.link,
                "feed": feed.get("id"),
                "title": post.title,
                "original_image": image,
                "description": post.description,
                "date": post.published_parsed,
                "image": image,
            }
    return articles
