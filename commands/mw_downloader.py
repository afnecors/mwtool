#!/usr/bin/python3
import click

def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()

@click.command()
@click.option(
    '-p', '--pagename',
    type=click.STRING,
    help="Title of an article")
@click.option(
    '-f', '--filename',
    type=click.Path(exists=True),
    help="Path to file containing a list of pages (one page per line)")
@click.option(
    '-t', '--top_pages',
    type=click.INT,
    help="Number of pages with the most revisions")
@click.option(
    '-r', '--random_pages',
    type=click.INT,
    help="Number of random pages")
@click.option(
    '-c', '--category_pages',
    type=click.STRING,
    help="Title of a category")
@click.pass_context
def downloader(
    ctx,
    pagename,
    filename,
    top_pages,
    random_pages,
    category_pages
    ):
    """
    Download MediaWiki page history
    """

    if pagename:
        click.echo('Download pagename ' + pagename)
        # Download the revision of the page
        # save to a csv
        pass

    if filename:
        click.echo('Download from file ' + filename)
        # Check if file exists
        # Check if file has a valid content
        # For each title in file
        # # download all revisions
        # # save to csv 
        pass

    if top_pages:
        click.echo('Download top_pages ' + str(top_pages) )
        pass

    if random_pages:
        click.echo('Download random_pages ' + str(random_pages) )
        pass

    if category_pages:
        click.echo('Download category_pages ' + category_pages)
        pass

    if (pagename is None and 
        filename is None and
        top_pages is None and
        random_pages is None and
        category_pages is None):
        print_help()

