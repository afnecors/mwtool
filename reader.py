#!/usr/bin/python3

from typing import List

import mwclient
import click
import csv
import os


DB_PATH = "./db"

class MWReader():

    def __init__(self, start_date, end_date, report_csv=False,
                 chart=False):
        self.report_csv = report_csv
        self.chart = chart
        self.start_date = start_date
        self.end_date = end_date
        pass

    def analyze_files_from_pageids_list(self, pageids):
        print('Analizzo')
        
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
        print(file_name)
        self.read_csv(file_name)
        pass

    def read_csv_pageid(self, pageid):
        pass

    def read_csv(self, file_name):
        pagename = ''
        revisions = []

        with open(DB_PATH + "/" + file_name + ".csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:

                # save pagename
                if line_count == 1:
                    pagename = row[1]
                # save revision
                if line_count > 1:
                    revisions.append(row)

                line_count += 1
                
            print('Page: ' + pagename + ' has ' + str(line_count) + ' revisions')

        self.calculate_measure(revisions)

        pass


    def calculate_measure(self, revisions):
        print('Calculate!\n')

        if self.chart == True:
            print('Generate chart!')

        if self.report_csv == True:
            print('Generate report!')

        pass
