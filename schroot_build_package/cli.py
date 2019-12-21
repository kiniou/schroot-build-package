import daiquiri
import logging
import click
import click_completion

daiquiri.setup()
log = logging.getLogger()
click_completion.init()


@click.group()
@click.option('-v', '--verbose/--no-verbose',
              help="verbose logging",
              default=False)
@click.option('-d', '--debug/--no-debug',
              help="debug logging",
              default=False)
def main(verbose, debug):
    """opinionated sbuild alternative"""
    if verbose:
        log.setLevel(logging.INFO)
    elif debug:
        log.setLevel(logging.DEBUG)
    log.info("Activating INFO logging")
    log.debug("Activating DEBUG logging")


@main.command('build')
@click.argument("PATH")
def build(path):
    log.info("building %s", path)
    pass


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
