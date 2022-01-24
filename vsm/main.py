"""
Main file
"""

# standard lib
import sys
from pathlib import Path

# package
from vsm import Config
from vsm.session_manager import VimSessionManager
from vsm.utils import ShellManager
from vsm.cli import Cli
from vsm.log import Log

# 3rd party
from result import Ok, Err


def main() -> int:
    """
    @description: executor function

    @retuns: exit status
    """
    shell = ShellManager()
    # preflight checks
    # TODO: Linux should be checked as os, distro information could be stored,
    # and vim variants checked for existence in an Initializer class, possible feature flag
    if not shell.is_installed("nvim") and not shell.is_installed("vim"):
        Log.error("No variant of vim was found on your system")
        return 1

    cli = Cli()
    vsm = VimSessionManager()
    if cli.args.list_sessions:
        vsm.list_sessions()

    elif cli.args.remove_session:
        session = Path(cli.args.remove_session)
        match vsm.remove_session(session):
            case Ok(value):
                Log.warn(f"Removing session -> {value}")
                # TODO: use a yes/no prompt to verify the user doesn't remove a file by accident
                value.unlink()
                Log.info("Done..")
            case Err(e):
                Log.error(e)
                return 1

    elif cli.args.open_session:
        session = Path(cli.args.open_session)
        match vsm.open_session(session):
            case Ok(value):
                Log.info(f"Loading session -> {value}")
                match shell.execute(f"nvim -S {value}"):
                    case Ok(_):
                        return 0
                    case Err(fail):
                        Log.error(fail)
                        return 1
            case Err(e):
                Log.error(e)
                return 1

    elif cli.args.the_current_state_of_things:
        Log.warn(f"This feature is currently under development")

    else:
        Log.error(
            f"No arguments give, please use `{Config.package()} --help` for usage information")
        return 1

    return 0


if __name__ == "__main__":
    status: int = main()
    sys.exit(status)
