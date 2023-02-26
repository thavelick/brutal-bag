"get favicon urls"

from html.parser import HTMLParser
import urllib.parse
import httpx


class FaviconParser(HTMLParser):
    "Find favicon URLs in HTML"

    def __init__(self, source_url):
        super().__init__()
        self.favicon_url = None
        self.source_url = source_url

    def handle_starttag(self, tag, attrs):
        if tag == "link" and (
            ("rel", "icon") in attrs or ("rel", "shortcut icon") in attrs
        ):
            self.favicon_url = dict(attrs)["href"]
            if not urllib.parse.urlparse(self.favicon_url).netloc:
                self.favicon_url = urllib.parse.urljoin(
                    self.source_url, self.favicon_url
                )


async def get_favicon_url(article_url):
    "Get the favicon URL for an article URL"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(article_url)

        except (httpx.ConnectError, httpx.ConnectTimeout):
            return None

        parser = FaviconParser(article_url)
        parser.feed(response.text)
        if parser.favicon_url:
            return parser.favicon_url
        else:
            site_url = article_url.split("/", 3)[2]

            standard_favicon_url = f"https://{site_url}/favicon.ico"
            try:
                response = await client.head(standard_favicon_url)
                # some sites have a 0 byte favicon.ico, so check the content length
                if response.headers.get("content-length") == "0":
                    return None

            except (httpx.ConnectError, httpx.ConnectTimeout):
                return None

            return standard_favicon_url
