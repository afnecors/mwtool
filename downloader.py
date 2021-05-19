#!/usr/bin/python3


class MWDownloader():

    def __init__(self):

        pass

    def download_page(self, pagename):
        print('Download page ' + pagename)
        # page = {}
        # self.save_page_to_csv()
        pass

    def dowload_from_file(self, filename):
        # Check if file exists
        # Check if file has a valid content
        # For each title in file
        # # download all revisions
        # # save to csv

        page_names = []
        with open(filename, 'r') as reader:
            for row in reader:
                current = row.rstrip('\n')
                page_names.append(current)

        for p in page_names:
            self.download_page(p)

        pass

    def download_top_pages(self, number):
        page_names = self.get_top_pages_names(number)
        for p in page_names:
            self.download_page(p)
        pass

    def download_random_pages(self, number):
        page_names = self.get_random_pages_names(number)
        for p in page_names:
            self.download_page(p)
        pass

    def download_from_category(self, category):
        page_names = self.get_category_pages_names(category)
        for p in page_names:
            self.download_page(p)
        pass

    # ------------------- #

    def get_top_pages_names(self, number):
        return [str(i) for i in range(number)]

    def get_random_pages_names(self, number):
        return [str(i) for i in range(number)]

    def get_category_pages_names(self, category):
        return ['Page1 in category ' + category, 'Page2 in category ' + category]

    # def save_page_to_csv():
    #     print('Saving page to csv')
    #     pass
