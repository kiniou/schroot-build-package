"""Shared functions and fixtures"""
from subprocess import run
import pytest


@pytest.fixture
def cmd_run():
    """Shared run command."""
    def _cmd_run(*args, **kwargs):
        return run(*args, **kwargs)  # pylint: disable=subprocess-run-check

    return _cmd_run


@pytest.fixture()
def ensure_chroot_is_deleted():
    run("sudo rm -rf /tmp/chroots", shell=True, check=False)
    yield
    run("sudo rm -rf /tmp/chroots", shell=True, check=False)
