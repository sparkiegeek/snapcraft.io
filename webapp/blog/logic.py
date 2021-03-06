import re
import html

from datetime import datetime


def strip_excerpt(raw_html):
    """Remove tags from a html string

    :param raw_html: The HTML to strip

    :returns: The stripped string
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return html.unescape(cleantext).replace('\n', '')


def transform_article(article, featured_image=None, author=None):
    """Transform article to include featured image, human readable
    date and a stipped version of the excerpt

    :param article: The raw article object
    :param featured_image: The featured image string

    :returns: The transformed article
    """
    article['image'] = featured_image

    article['author'] = author

    if 'date_gmt' in article:
        article_gmt = article['date_gmt']
        article_date = datetime.strptime(article_gmt, '%Y-%m-%dT%H:%M:%S')
        article['date'] = article_date.strftime('%-d %B %Y')

    if 'excerpt' in article and 'rendered' in article['excerpt']:
        article['excerpt']['raw'] = strip_excerpt(
            article['excerpt']['rendered'])[:340]

        # If the excerpt doesn't end before 340 characters, add ellipsis
        raw_article = article['excerpt']['raw']
        # split at the last 3 characters
        raw_article_start = raw_article[:-3]
        raw_article_end = raw_article[-3:]
        # for the last 3 characters replace any part of […]
        raw_article_end = raw_article_end.replace('[', '')
        raw_article_end = raw_article_end.replace('…', '')
        raw_article_end = raw_article_end.replace(']', '')
        # join it back up
        article['excerpt']['raw'] = ''.join([
            raw_article_start,
            raw_article_end,
            ' […]'])

    return article


def change_url(feed, host):
    """Change insights urls to snapcraft.io/blog

    :param feed: String with urls

    :returns: A string with converted urls
    """
    url_regex = re.compile(
        'https:\/\/admin.insights.ubuntu.com(\/\d{4}\/\d{2}\/\d{2})?')
    updated_feed = re.sub(url_regex, host, feed)

    return updated_feed
