import click
import logging
from subprocess import run, PIPE
from pathlib import Path
import csv
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
    log.info("creating schroot %s in %s", suite, schroots)
    

@schroot.command('list-suites')
@click.option('--vendor', metavar="VENDOR",
              type=click.Choice(_available_vendors))
def list_suites(vendor):
    """List available vendors and suites"""
    if vendor is None:
        vendors = _available_vendors
    else:
        vendors = [vendor]
    for v in vendors:
        print(v)
        csv_path = Path("/usr/share/distro-info/{0}.csv".format(v))
        with csv_path.open() as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:
                print("- {0} - {1}".format(line.get('series'),
                                           line.get('codename')))
