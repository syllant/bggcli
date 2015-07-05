#! /usr/bin/env python
"""
Command Line Interface for BoardGameGeek.com

Usage: bggcli   [--version] [-v] [-l <login>] [-p <password>]
                [-c <name>=<value>]...
                <command> [<args>...]

Options:
    --version                       Show version of this tool
    -v                              Activate verbose logging
    -l, --login <login>             Your login on BGG
    -p, --password <password>       Your password on BGG
    -c <name=value>                 To specify advanced options, see below

Advanced options:
    browser-keep=<true|false>       If you want to keep your web browser opened at the end of the
                                    operation
    browser-profile-dir=<dir>       Path or your browser profile if you want to use an existing
                                    profile (useful for debugging purpose)

Available commands are:
   help                 Display general help or help for a specific command
   collection-import    Import a game collection from a CSV file
   collection-export    Export a game collection as a CSV file
   collection-delete    Delete games in a collection

See 'bggcli help <command>' for more information on a specific command.
"""
import sys
import time

from selenium.common.exceptions import WebDriverException

from docopt import docopt

from bggcli import UI_ERROR_MSG
from bggcli.util.logger import Logger
from bggcli.version import VERSION


def import_command_module(name):
    return __import__('bggcli.commands.%s' % name.replace('-', '_'), fromlist=['bggcli.commands'])


def exit_unknown_command(command):
    exit_error('Unknown command: %s. See usage:\n' % command, ['-h'])


def exit_error(msg, args):
    Logger.error(msg)
    Logger.error(docopt(__doc__, args))
    exit(1)


def explode_dyn_args(l):
    return {k: v for k, v in (x.split('=') for x in l)}


def show_help(command_args):
    if len(command_args) > 0:
        help_command = command_args[0]
        try:
            command_module = import_command_module(help_command)
            Logger.info(docopt(command_module.__doc__, ['-h']))
        except ImportError:
            exit_unknown_command(help_command)
    else:
        Logger.info(docopt(__doc__, argv=['-h']))


def main():
    _main(sys.argv[1:])


def _main(argv):
    # Don't find any good git command-like parser in Python with user-friendly error
    # management, docopt is (too) simple
    if not argv:
        argv = ['help']

    args = docopt(__doc__, argv, version='bggcli %s' % VERSION, options_first=True)

    command = args['<command>']

    Logger.isVerbose = args.get('-v')

    if command == 'help':
        show_help(args['<args>'])
    else:
        execute_command(command, argv)


def parse_commad_args(command_module, argv):
    result = docopt(command_module.__doc__, argv, version='bggcli %s' % VERSION,
                    options_first=False)

    try:
        return result, explode_dyn_args(result['-c'])
    except StandardError:
        Logger.info('Invalid syntax for -c option, should be "-c key=value"!')
        return None


def show_duration(timer_start):
    m, s = divmod(time.time() - timer_start, 60)
    h, m = divmod(m, 60)
    if h > 0:
        Logger.info("(took %d:%02d:%02d)" % (h, m, s))
    else:
        Logger.info("(took %02d:%02d)" % (m, s))


def execute_command(command, argv):
    timer_start = time.time()

    try:
        command_module = import_command_module(command)
        command_args, command_args_options = parse_commad_args(command_module, argv)

        if command_args:
            command_module.execute(command_args, command_args_options)
            show_duration(timer_start)
    except ImportError:
        exit_unknown_command(command)
    except WebDriverException as e:
        Logger.error(UI_ERROR_MSG, e)
    except Exception as e:
        Logger.error("Encountered an unexpected error, please report the issue to the author", e)


if __name__ == '__main__':
    main()
