#!/usr/bin/python3

import mwclient
import click
import csv
import os
import calendar
import requests
from bs4 import BeautifulSoup as bs

CSV_FILEDS = [
    'pageid',
    'title',
    'revid',
    'parentid',
    'timestamp',  # UTC Time
    'flags',
    'comment',
    'commenthidden', # only if no comment
    'user',
    'userhidden', # only if no user
    'userid',
    'size',
    'tags',
    'minor'
]

DB_PATH = './db'

def get_last_revision_id_from_file(filepath):
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        first_data = list(reader)[-1]
        return first_data['revid']

def save_csv(id, title, rows):
    """
    Save data in csv file
    - 1st line: csv header
    - 2nd line: row with pageid and title filled
    - other lines: one row per revision
    """
    dir_path = DB_PATH
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    with open(dir_path + "/" + str(id) + ".csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(CSV_FILEDS)

        # add page id and title in first data row
        first_data_row = dict(pageid=id, title=title)
        rows.insert(0, first_data_row)

        for row in rows:
            targetrow = []
            for key in CSV_FILEDS:
                try:
                    if key == 'timestamp':
                        time_epoch = calendar.timegm(row[key])
                        targetrow.append(time_epoch)
                    else:
                        targetrow.append(row[key])
                except KeyError:
                    targetrow.append('')
                    pass
            writer.writerow(targetrow)

    pass


def append_to_existing_csv(filepath, new_rows):
    # se il file esiste deve avere almeno una revision
    with open(filepath, 'a') as csvfile:
        writer = csv.writer(csvfile)

        for row in new_rows:
            targetrow = []
            for key in CSV_FILEDS:
                try:
                    if key == 'timestamp':
                        time_epoch = calendar.timegm(row[key])
                        targetrow.append(time_epoch)
                    else:
                        targetrow.append(row[key])
                except KeyError:
                    targetrow.append('')
                    pass
            writer.writerow(targetrow)
    pass

class MWDownloader():
    prop_revisions = 'ids|timestamp|flags|comment|user|userid|size|tags'

    def __init__(self):
        self.mw_pages = MWPages()

    def download_page(self, pagename):
        print('Download page ' + pagename)
        page = self.mw_pages.get_page(pagename)

        # controlla se la pagina è già stata scaricata
        # precedentemente nella cartella /db
        filepath = DB_PATH + '/' + str(page.pageid) + '.csv'
        if os.path.isfile(filepath):
            # file exist
            last_rev_id = get_last_revision_id_from_file(filepath)
            revisions_to_append = page.revisions(
                limit=500, dir='newer', prop=self.prop_revisions, startid=last_rev_id)

            # tolgo la prima revision per evitare duplicati
            revision_list = list(revisions_to_append)[1:]

            # se ci sono nuove revision le appendo al file già presente
            if len(revision_list) > 0:
                append_to_existing_csv(filepath, revision_list)
        else:
            # file not exist
            revisions = page.revisions(
                limit=500, dir='newer', prop=self.prop_revisions)

            save_csv(page.pageid, page.page_title, list(revisions))
        pass

    def dowload_from_file(self, filename):
        page_names = []
        with open(filename, 'r') as reader:
            for row in reader:
                current = row.rstrip('\n')
                page_names.append(current)

        for p in page_names:
            self.download_page(p)
        pass

    def download_top_pages(self, number):
        page_names = self.__get_top_pages_names(
            number)
        for p in page_names:
            self.download_page(p)
        pass

    def download_random_pages(self, number):
        page_names = self.__get_random_pages_names(number)
        for p in page_names:
            self.download_page(p)
        pass

    def download_from_category(self, category):
        page_names = self.__get_category_pages_names(category)
        for p in page_names:
            self.download_page(p)
        pass

    # private methods
    def __get_top_pages_names(self, limit):
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

    def __get_random_pages_names(self, number):
        return self.mw_pages.get_random(number)

    def __get_category_pages_names(self, category):
        return self.mw_pages.get_pages_in_cat(category)


class MWPages(object):

    def __init__(self):
        self.site = mwclient.Site('en.wikipedia.org')

    def get_page(self, title: str) -> mwclient.page.Page:
        """
        Get a single page.
        """
        page = self.site.pages[title]
        if page.exists:
            return page
        else:
            raise click.UsageError('Page not found!')

    def get_random(self, number):
        """
        Get a random list of pages names
        """
        pages_gen = self.site.random(0, limit=number)
        page_names = []
        for i in range(number):
            page = next(pages_gen)
            page_names.append(page['title'])
        return page_names

    def get_pages_in_cat(self, catname):
        """
        Get a list of pages names in a category
        """
        cat = self.site.categories[catname]
        page_names = []
        for c in cat:
            if c.namespace == 0:
                page_names.append(c.page_title)
            # sub-category
            # Category namespace is 14 in MediaWiki
            #  
            if c.namespace == 14:
                # TODO gestire le sottoactegorie
                # 
                pass
        return page_names


# Revert as metric