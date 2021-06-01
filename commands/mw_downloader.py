#!/usr/bin/python3
import click
import downloader as mwd

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

    mwDownloader = mwd.MWDownloader()

    if pagename:
        mwDownloader.download_page(pagename)
        pass

    if filename:
        # click.echo('Download from file ' + filename)
        mwDownloader.dowload_from_file(filename)
        pass

    if top_pages:
        # click.echo('Download top_pages ' + str(top_pages) )
        mwDownloader.download_top_pages(top_pages)
        pass

    if random_pages:
        # click.echo('Download random_pages ' + str(random_pages) )
        mwDownloader.download_random_pages(random_pages)
        pass

    if category_pages:
        # click.echo('Download category_pages ' + category_pages)
        if category_pages.startswith('Category:'):
            category_pages = category_pages[9:]
        mwDownloader.download_from_category(category_pages)
        pass

    if (pagename is None and 
        filename is None and
        top_pages is None and
        random_pages is None and
        category_pages is None):
        print_help()

