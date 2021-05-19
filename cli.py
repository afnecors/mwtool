#!/usr/bin/python3
import click
import commands.mw_analyzer as a
import commands.mw_downloader as d

@click.group()
def run():
    """
    For more detailed help run "mwtool [command name] --help"
    """
    pass

run.add_command(d.downloader)
run.add_command(a.analyzer)

if __name__ == '__main__':
    run()
