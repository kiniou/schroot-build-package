"""test_schroot - Tests related to the schroot subcommand"""
import logging
from pathlib import Path
from subprocess import PIPE
import pytest

log = logging.getLogger(__name__)


def test_sbp_is_installed(cmd_run):
    """Check if `sbp` command is installed"""
    result = cmd_run([
        "sbp"
    ])
    log.debug(result)
    assert result.returncode == 0, "`sbp` command does not seems correctly installed!"


def test_list_suites(cmd_run):
    """Check if we can list available suites."""
    cmd = ["sbp", "schroot", "list-suites"]
    result = cmd_run(cmd, stdout=PIPE)
    log.debug(result.stdout.decode())
    assert result.returncode == 0, ("Can not list schroot suites with command %s!"
                                    % (" ".join(cmd)))


@pytest.mark.slow
def test_create(cmd_run, ensure_chroot_is_deleted):
    """Check if we can create a simple schroot"""
    cmd = "sudo $(command -v sbp) schroot create sid /tmp/chroots"
    result = cmd_run(cmd, shell=True, stdout=PIPE)
    log.debug(result.stdout.decode())
    assert Path('/tmp/chroots/sid-amd64').exists() is True, "chroot does not exists!"
    cmd_run("sudo rm -rf /tmp/chroots", shell=True)
    assert result.returncode == 0, ("Can not create requested schroot with command %s!"
                                    % (cmd))
