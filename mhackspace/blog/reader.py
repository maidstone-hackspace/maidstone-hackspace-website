import feedparser

urls = [
    'https://feeds.feedburner.com/projects-jl',
    'https://hackaday.com/tag/emf-camp-2018/feed/',
    'https://maidstone-hackspace.org.uk/blog/rss/',
    'http://webboggles.com/feed/',
    'https://blog.digitaloctave.com/rss.xml',
]

for url in urls:
    print(url)
    parsed = feedparser.parse(url)

    for post in parsed.entries:
        print(post.title)
