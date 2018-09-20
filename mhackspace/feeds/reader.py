import lxml
import feedparser
import datetime
from io import StringIO
from operator import itemgetter
from lxml.html.clean import Cleaner

from django.utils.html import escape

filter_by_date_expire = datetime.datetime.now() - datetime.timedelta(
    days=int(1.5 * 365)
)


def filter_by_tags(self, node, tags=None):
    """filter the feed out by category tag, if no tags assume its pre filtered"""
    if self.tags is None:
        return True
    for category in node.xpath("./category", namespaces=namespaces):
        if category.text.lower() in self.tags:
            return True
    return False


def filter_by_date(self, date):
    """filter the feed out by date"""
    if self.enable_date_filter is False:
        return True
    if date > self.filter_by_date_expire:
        return True
    return False


def parse_content(content):
    html_img_cleaner = Cleaner(allow_tags=["img"], remove_unknown_tags=False)
    html_img_cleaner.allow_tags = ["img"]

    xml_parser = lxml.etree.XMLParser(
        remove_blank_text=True, ns_clean=True, encoding="utf-8"
    )

    return lxml.etree.XML("<div>" + escape(content) + "</div>", xml_parser)


def fetch_image_from_node_text(text):
    html_parser = lxml.etree.HTMLParser()
    description = lxml.etree.parse(StringIO(text), html_parser)
    for image in description.xpath(".//img"):
        return image.get("src")
    return None


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
    image = fetch_image_from_node_text(post.description)
    if image:
        return image

    # no image so lets fall back to the channel image if it exists
    return None


def fetch_feeds(feeds):
    articles = {}

    print(feeds)
    for feed in feeds:
        url = feed.get("url")
        author = feed.get("author")
        parsed = feedparser.parse(url)
        namespaces = {}
        if hasattr(parsed, "namespaces"):
            namespaces = parsed.namespaces
        feed_image = ""
        if hasattr(parsed.feed, "image"):
            feed_image = parsed.feed.image.get("href")
        print(author)
        for post in parsed.entries:
            root_node = parse_content(post.description)
            image = fetch_image(post, root_node, namespaces) or feed_image

            articles.setdefault(author, []).append(
                {
                    "url": post.link,
                    "feed": feed.get("id"),
                    "title": post.title,
                    "original_image": image,
                    "description": post.description,
                    "date": post.published_parsed,
                    "image": image,
                }
            )

    # order authors articles by date
    for author in articles.keys():
        articles[author] = sorted(
            articles[author], key=itemgetter("date"), reverse=True
        )
    return [f for f in alternate_dict_and_sort_by_list_item_key(articles)]

    # return articles


def alternate_dict_and_sort_by_list_item_key(dict_of_lists, sort_key="date"):
    """ take a dictonary of ordered lists, step through each row and sort the current
    item position in each list and yield the result.

    basically gives the ordering of date while stepping through the blog entries to make it fair
    for people who do not blog often. """
    longest_list_length = max(
        [len(dict_of_lists[d]) for d in dict_of_lists.keys()] + [0]
    )

    # order each feed by date, newest date at the end of the list so it can be poped
    for author in dict_of_lists:
        dict_of_lists[author].sort(key=itemgetter("date"), reverse=False)

        # now iterate through author lists, popping the first elements and order the current item
        # from each list by date
        for i in range(0, longest_list_length):
            # get first value from each key, and order the list by sort key which is date by default
            feed_row = [d.pop() for d in dict_of_lists.values() if d]
            results = sorted(feed_row, key=itemgetter(sort_key), reverse=True)
            for item in results:
                yield item
