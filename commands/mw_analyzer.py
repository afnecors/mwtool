#!/usr/bin/python3
import click
from datetime import date

import reader as mw_reader
import downloader as mw_downloader


def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    click.echo("\nYou must choose -o or -d mode!")
    ctx.exit()

@click.command()
@click.option(
    '-o', '--output-csv',
    is_flag=True,
    help="MODE: Generate csv report")
@click.option(
    '-d', '--diagram',
    is_flag=True,
    help="MODE: Generate diagram report")
@click.option(
    '-s', '--start-date',
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date(2001, 1, 15)),
    help="Start date string in following format: %Y-%m-%d")  # %Y-%m-%d
@click.option(
    '-e', '--end-date',
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="Start date string in following format:%Y-%m-%d")  # %Y-%m-%d
@click.option(
    '-p', '--pagename',
    type=click.STRING,
    help="Analyses single page")
@click.option(
    '-f', '--filename',
    type=click.Path(exists=True),
    help="Analyses pages from a file containing a list of them (one title per line)")
@click.option(
    '-t', '--top_pages',
    type=click.INT,
    help="Analyses pages with the most revisions")
@click.option(
    '-r', '--random_pages',
    type=click.INT,
    help="Analyses random pages")
@click.option(
    '-c', '--category_pages',
    type=click.STRING,
    help="Analyses a category")
@click.option(
    '-a', '--all',
    is_flag=True,
    help="Analyses all previously downloaded pages")
def analyzer(
    output_csv,
    diagram,
    start_date,
    end_date, pagename, filename, top_pages, random_pages, category_pages, all):
    """
    Analyze MediaWiki page history
    """

    # Report e diagram sono le due modalità
    # Altrimenti stampa l'help
    if (output_csv == False and diagram == False):
        print_help()

    # inizializza il downloader
    # si occupa lui di verificare se le voci sono già state scaricate
    mwDownloader = mw_downloader.MWDownloader()

    # ---- DOWNLOADER ---- #
    if pagename:
        mwDownloader.download_page(pagename)
        pass

    if filename:
        click.echo('Download pages from file ' + filename)
        mwDownloader.dowload_from_file(filename)
        pass

    if top_pages:
        click.echo('Download top ' + str(top_pages) + ' pages')
        mwDownloader.download_top_pages(top_pages)
        pass

    if random_pages:
        click.echo('Download ' + str(random_pages) + ' random pages')
        mwDownloader.download_random_pages(random_pages)
        pass

    if category_pages:
        if category_pages.startswith('Category:'):
            category_pages = category_pages[9:]
        click.echo('Download pages from Category:' + category_pages)
        mwDownloader.download_from_category(category_pages)
        pass
    # ---- DOWNLOADER ---- #

    # ---- ANALISI DATI ---- #
    mwReader = mw_reader.MWReader(start_date, end_date, output_csv,
                                  diagram)

    pageids = []
    if all:
        pageids = mwReader.get_list_of_file_to_analyze()
    else:
        pageids = mwDownloader.get_downloaded_pages_ids()

    if len(pageids) > 0:
        mwReader.analyze_files_from_pageids_list(pageids)

        # TODO
        if output_csv:
            click.echo('Generate csv report')
            pass

        if diagram:
            click.echo('Generate diagram report')
            pass

        if start_date and end_date:
            # click.echo('Start date ' + str(start_date.date()) )
            # click.echo('End date ' + str(end_date.date()) )
            pass

    
    

