"""schroot cli commands"""
import logging
from pathlib import Path
import csv

import click
from tabulate import tabulate

from .cli import main

log = logging.getLogger()
_available_vendors = ['debian', 'ubuntu']


@main.group()
def schroot():
    """schroot related commands"""


@schroot.command()
@click.option('--arch', metavar="ARCHITECTURE", default="amd64")
@click.argument('SUITE')
@click.argument('SCHROOTS', required=False, default='/var/lib/schroot')
def create(arch, suite, schroots):
    """Bootstrap a schroot with a recognized debootstrap SUITE
    under the SCHROOTS path.

    See /usr/share/debootstrap for a complete list of available deboostrap suites.
    """
    log.info("creating schroot %s(%s) in %s", suite, arch, schroots)


def add_vendor_to_list(vendor, items):
    """Prepend vendor column to a csv DictReader"""
    for item in items:
        item['vendor'] = vendor
        item.move_to_end('vendor', last=False)
        log.debug(item)
        yield item


def keep_columns(items, columns_to_keep):
    """Keep selected columns in a csv DictReader."""
    for item in items:
        new_item = item.copy()
        keys = item.keys()
        for column in keys:
            log.debug(column)
            if column not in columns_to_keep:
                del new_item[column]
        yield new_item.copy()


@schroot.command('list-suites')
@click.option('--vendor', metavar="VENDOR",
              type=click.Choice(_available_vendors))
def list_suites(vendor):
    """List available vendors and suites"""
    if vendor is None:
        vendors = _available_vendors
    else:
        vendors = [vendor]
    for vendor_iter in vendors:
        csv_path = Path("/usr/share/distro-info/{0}.csv".format(vendor_iter))
        with csv_path.open() as csv_file:
            reader = csv.DictReader(csv_file)
            print(tabulate(
                add_vendor_to_list(vendor_iter, keep_columns(reader, ['version',
                                                                      'codename',
                                                                      'release',
                                                                      'eol'])),
                headers="keys"))
        if vendor_iter != vendors[-1]:
            print()
