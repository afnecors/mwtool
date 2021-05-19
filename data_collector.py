#!/usr/bin/python3

import mwclient
import requests
import click
from bs4 import BeautifulSoup as bs
from typing import List

def get_top_pages_titles(limit: int = 50) -> List[str]:
    url = "https://en.wikipedia.org/w/index.php?title=Special:MostRevisions"
    url += "&limit=" + str(limit)
    page = requests.get(url)

    if page.ok:
        soup = bs(page.content, 'html.parser')
        links_list = soup.select("ol > li > a:first-child")
        articles = [link.get_text() for link in links_list]
        return articles
    else:
        return []

class MWDataCollector:

    def __init__(self):
        self.site = mwclient.Site('en.wikipedia.org')
        pass

    def get_page(self, title: str) -> mwclient.page.Page:
        """
        Get a single page.
        """
        page = self.site.pages[title]
        if page.exists:
            return page
        else:
            raise click.UsageError('Page not found!')

    def get_pages_from_category(self, category_name) -> List[mwclient.page.Page]:
        """
        Get a list of pages from a category.
        Only one level and only ns 0 pages.
        """
        category_page = self.site.categories[category_name]
        if category_page.exists:
            result_pages_list = []
            for page in category_page:
                if page.namespace == 0:
                    result_pages_list.append(page)
                # if page.namespace == 14: is a category
            return result_pages_list
        else:
            raise click.UsageError('Category not found!')

    def get_random_pages(self, number: int) -> List[mwclient.page.Page]:
        page_generator = self.site.random(namespace=0)
        pages = [next(page_generator) for x in range(number)]
        return pages

    def get_top_pages(self, limit) -> List[mwclient.page.Page]:
        titles = get_top_pages_titles(limit)
        pages = []
        for title in titles:
            page = self.get_page(title)
            pages.append(page)
        return pages
        