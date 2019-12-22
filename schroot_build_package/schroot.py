"""schroot cli commands"""
from collections import OrderedDict
import csv
import logging
import os
from pathlib import Path
from subprocess import run
import sys

import click
from tabulate import tabulate

from .cli import main

log = logging.getLogger()
AVAILABLE_VENDORS = ['debian', 'ubuntu']


@main.group("schroot")
def schroot_group():
    """schroot cli commands"""


@schroot_group.command('create', short_help="bootstrap a chroot environment")
@click.option('--arch', metavar="ARCHITECTURE", default="amd64")
@click.option('--variant', type=click.Choice(['buildd', 'minbase']), default='minbase')
@click.argument('SUITE')
@click.argument('SCHROOTS', required=False, default='/var/lib/schroot')
def create_schroot(arch, variant, suite, schroots):
    """Bootstrap a schroot with a recognized debootstrap SUITE
    under the SCHROOTS path.

    See /usr/share/debootstrap for a complete list of available deboostrap suites.
    """
    # TODO: explore the value of using `proot` instead of `debootstrap` ()
    schroot_path = Path(schroots) / "{0}-{1}".format(suite, arch)
    log.info("creating schroot %s(%s) in %s", suite, arch, schroot_path)

    if os.getuid() != 0:
        log.error("Must be root !!!")

    if schroot_path.exists():
        log.error("%s already exists !!! (Hint: remove it first with a good old «rm -rf %s»)",
                  schroot_path, schroot_path)
        sys.exit(1)

    result = run(['debootstrap', '--variant={0}'.format(variant), suite, schroot_path],
                 check=False)

    sys.exit(result.returncode)


def add_vendor_to_list(vendor, items):
    """Prepend vendor column to a csv DictReader"""
    for item in items:
        item['vendor'] = vendor
        item.move_to_end('vendor', last=False)
        log.debug(item)
        yield item


def keep_columns_and_reorder(items, columns_to_keep):
    """Keep selected columns in a csv DictReader and reorder them."""
    for item in items:
        new_item = OrderedDict()
        for column in columns_to_keep:
            log.debug(column)
            if column in columns_to_keep:
                new_item[column] = item[column]
        yield new_item


@schroot_group.command('list-suites', short_help="list available suites to bootstrap")
@click.option('--vendor', metavar="VENDOR",
              type=click.Choice(AVAILABLE_VENDORS))
def list_suites(vendor):
    """List available vendors and suites"""
    if vendor is None:
        vendors = AVAILABLE_VENDORS
    else:
        vendors = [vendor]
    for vendor_iter in vendors:
        csv_path = Path("/usr/share/distro-info/{0}.csv".format(vendor_iter))
        with csv_path.open() as csv_file:
            reader = csv.DictReader(csv_file)
            print(
                tabulate(
                    add_vendor_to_list(vendor_iter,
                                       keep_columns_and_reorder(reader, ['series',
                                                                         'version',
                                                                         'codename',
                                                                         'release',
                                                                         'eol'])),
                    headers="keys")
            )
        if vendor_iter != vendors[-1]:
            print()
