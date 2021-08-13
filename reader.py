#!/usr/bin/python3

from typing import List

import mwclient
import click
import csv
import os

import re

import mw_analysis_util


DB_PATH = "./db"

def remove_bots(revisions):
    """
    This function removes all revisions from a list
    that contain 'bot' in username
    (regex: [Bb][oO][Tt] for last three characters)
    """
    revisions_without_bots = []

    for r in revisions:
        username = r['user'] or r['userhidden']
        is_bot = re.match('[Bb][oO][Tt]', username[-3:])
        if (not bool(is_bot)):
            revisions_without_bots.append(r)
        
    return revisions_without_bots

class MWReader():

    def __init__(self, start_date, end_date, report_csv=False,
                 chart=False):
        self.report_csv = report_csv
        self.chart = chart
        self.start_date = start_date
        self.end_date = end_date
        pass

    def analyze_files_from_pageids_list(self, pageids):
        
        for id in pageids:
            self.analyze_single_file(id)

        pass

    def get_list_of_file_to_analyze(self) -> List[str]:
        files = []
        if os.path.exists(DB_PATH):
            files = os.listdir(DB_PATH)
        else:
            files = []
            
        if len(files) == 0:
            click.echo('No files to analyze!')
        else:
            # remove all non csv files
            for el in files:
                if el[-4:] != ".csv":
                    files.remove(el)

        # remove .csv from file name, only pageid (1234.csv => 1234)
        return [ f[:-4] for f in files]  

    def analyze_single_file(self, file_name):
        # print(file_name)
        self.read_csv(file_name)

    def read_csv(self, file_name):
        pagename = ''
        revisions = []

        with open(DB_PATH + "/" + file_name + ".csv") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # save pagename
                if line_count == 0:
                    pagename = row['title']
                # save revision
                if line_count > 1:
                    revisions.append(row)

                line_count += 1
                
        self.calculate_measure(revisions, pagename)
    

    def calculate_measure(self, revisions, pagename):

        revisions_nobot = remove_bots(revisions)
        cancellation = mw_analysis_util.count_all_cancellation(revisions_nobot)
        
        if self.chart == True:
            print('Generate chart!')

        if self.report_csv == True:
            # print('Generate report!')

            print(pagename)
            print('Revision totali', len(revisions))
            print('Revision senza bot', len(revisions_nobot))
            print('Reverted', len(cancellation))
            print('')

