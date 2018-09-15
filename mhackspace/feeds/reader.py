import lxml
import feedparser
from operator import itemgetter
from lxml import etree
from lxml.html.clean import Cleaner
from io import StringIO, BytesIO

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
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0"
    }
    html_cleaner = Cleaner()
    html_cleaner.javascript = True
    html_cleaner.style = True
    html_cleaner.remove_tags = [
        "script",
        "iframe",
        "link",
        "style",
        "img",
        "div",
    ]
    # ~ html_cleaner.allow_tags = ['a', 'p', 'strong']

    html_img_cleaner = Cleaner(allow_tags=["img"], remove_unknown_tags=False)
    html_img_cleaner.allow_tags = ["img"]

    xml_parser = lxml.etree.XMLParser(
        remove_blank_text=True, ns_clean=True, encoding="utf-8"
    )

    print("------------------")
    print(content)

    dom = lxml.etree.XML("<div>" + content + "</div>", xml_parser)
    return dom


def fetch_image_from_node_text(text):
    description = lxml.etree.parse(text, html_parser)
    for image in description.xpath(".//img"):
        print('fetch image from node text')
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
        print('media')

        image = post.media_thumbnail
        print(image)

        if image:
            return image[0].get("url")

    if hasattr(post, "content"):
        print('content')
        content = " ".join(c.value for c in post.content)
        image = fetch_image_from_node_text(content)
        if image:
            return image

    # final attempt at getting an image from the item using description
    result = fetch_node_text(node, "description")
    if result:
        print('description')
        image = fetch_image_from_node_text(result)
        if image:
            return image

    # no image so lets fall back to the channel image if it exists
    return None


def fetch_feeds(feeds):
    for feed in feeds:
        url = feed.get('url')
        print(url)
        parsed = feedparser.parse(url)
        namespaces = {}
        if hasattr(parsed, "namespaces"):
            namespaces = parsed.namespaces
        feed_image = ""
        if hasattr(parsed.feed, "image"):
            feed_image = parsed.feed.image.get('href')
        articles = []
        for post in parsed.entries:
            print(post.published)
            print(feed_image)
            root_node = parse_content(post.description)
            image = fetch_image(post, root_node, namespaces) #or feed_image

            articles.append(
                {
                    "url": post.link,
                    "feed": feed.get('id'),
                    "title": post.title,
                    "original_image": image,
                    "description": post.description,
                    "date": post.published_parsed,
                    "image": feed_image,
                }
            )
            print(articles[-1])
    return articles
