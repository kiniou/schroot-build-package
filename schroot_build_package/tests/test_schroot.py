import logging
from subprocess import PIPE
log = logging.getLogger(__name__)


def test_sbp_installed(cmd_run):
    """Check if `sbp` command is installed"""
    result = cmd_run([
        "sbp"
    ])
    log.debug(result)
    assert result.returncode == 0, "`sbp` command does not seems correctly installed."


def test_schroot_create(cmd_run):
    cmd = ["sbp", "schroot", "create", "sid", "/tmp/sid-amd64"]
    result = cmd_run(cmd)
    log.debug(result)
    assert result.returncode == 0, ("Can not create requested schroot with command %s"
                                    % (" ".join(cmd)))


def test_schroot_list(cmd_run):
    cmd = ["sbp", "schroot", "list-suites"]
    result = cmd_run(cmd, stdout=PIPE)
    log.debug(result.stdout.decode())
    assert result.returncode == 0, ("Can not list schroot suites with command %s"
                                    % (" ".join(cmd)))
