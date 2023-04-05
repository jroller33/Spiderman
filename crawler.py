# crawler for IMDB

import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:

    def __init__(self, urls=[]):        # constructor
        self.visited_urls = []          # all URLs that have already been visited
        self.urls_to_visit = urls       # URLs that need to be visited

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):   # finds URLS on the site
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):                # filters the URLs and adds them to 'urls_to_visit' if it hasn't been visited yet and isn't already in 'urls_to_visit'
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):                       # this is the method that the crawler actually uses
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')        # logs URLs
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)           # adds URL to 'visited_urls'

if __name__ == '__main__':
    Crawler(urls=['https://www.imdb.com/']).run()       # defines start URL