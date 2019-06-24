import click
import logging

from .cli import main

log = logging.getLogger()


@main.group()
def schroot():
    """schroot related commands"""


@schroot.command()
@click.option('--arch', default="")
@click.argument('SUITE')
@click.argument('TARGET-DIRECTORY')
def create(arch, suite, target_directory):
    """create a shroot with options
    """
    log.info("creating schroot %s in %s", suite, target_directory)
