import pytest
from subprocess import run, PIPE


@pytest.fixture
def cmd_run():
    def _cmd_run(*args, **kwargs):
        return run(*args, **kwargs)

    return _cmd_run
