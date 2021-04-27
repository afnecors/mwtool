#!/usr/bin/python3
import click
from datetime import date

@click.command()
@click.option(
    '-r', '--report-csv',
    is_flag=True,
    help="Generate csv report")
@click.option(
    '-c', '--chart',
    is_flag=True,
    help="Generate chart report")
@click.option(
    '-s', '--start-date',
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="Start date string in following format: %Y-%m-%d")  # %Y-%m-%d
@click.option(
    '-e', '--end-date',
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=str(date.today()),
    help="Start date string in following format:%Y-%m-%d")  # %Y-%m-%d
def analyzer(
    report_csv,
    chart,
    start_date,
    end_date):
    """
    Analyze MediaWiki page history
    """

    if report_csv:
        click.echo('Generate csv report')
        pass

    if chart:
        click.echo('Generate chart report')
        pass

    if start_date and end_date:
        click.echo('Start date ' + str(start_date.date()) )
        click.echo('End date ' + str(end_date.date()) )
        pass

