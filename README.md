# mwtool

## Setup
```console
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install --editable .
Obtaining file:///home/francesco/Development/mwtool
Collecting click
  Using cached click-7.1.2-py2.py3-none-any.whl (82 kB)
Installing collected packages: click, mwtool
  Running setup.py develop for mwtool
Successfully installed click-7.1.2 mwtool
```

## Usage
```console
$ mwtool
Usage: mwtool [OPTIONS] COMMAND [ARGS]...

  For more detailed help run "mwtool [command name] --help"

Options:
  --help  Show this message and exit.

Commands:
  analyzer    Analyze MediaWiki page history
  downloader  Download MediaWiki page history
```

## mwtool analyzer
```console
$ mwtool analyzer --help
Usage: mwtool analyzer [OPTIONS]

  Analyze MediaWiki page history

Options:
  -r, --report-csv             Generate csv report
  -c, --chart                  Generate chart report
  -s, --start-date [%Y-%m-%d]  Start date string in following format: %Y-%m-%d
  -e, --end-date [%Y-%m-%d]    Start date string in following format:%Y-%m-%d
  --help                       Show this message and exit.
```

## mwtool downloader
```console
$ mwtool downloader --help
Usage: mwtool downloader [OPTIONS]

  Download MediaWiki page history

Options:
  -p, --pagename TEXT         Title of an article
  -f, --filename PATH         Path to file containing a list of pages (one
                              page per line)

  -t, --top_pages INTEGER     Number of pages with the most revisions
  -r, --random_pages INTEGER  Number of random pages
  -c, --category_pages TEXT   Title of a category
  --help                      Show this message and exit.
```

## Built With
- [Click](https://click.palletsprojects.com/en/7.x/) - Python package for creating command line interfaces