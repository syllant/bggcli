"""
Delete games in your collection from a CSV file. BE CAREFUL, this action is irreversible!

Usage: bggcli [-v] -l <login> -p <password>
              [-c <name>=<value>]...
              collection-delete [--force] <file>

Options:
    -v                              Activate verbose logging
    -l, --login <login>             Your login on BGG
    -p, --password <password>       Your password on BGG
    --force                         Force deletion, without any confirmation
    -c <name=value>                 To specify advanced options, see below

Advanced options:
    browser-keep=<true|false>       If you want to keep your web browser opened at the end of the
                                    operation
    browser-profile-dir=<dir>       Path or your browser profile if you want to use an existing

Arguments:
    <file> The CSV file with games to import
"""
import sys

from bggcli.commands import check_file
from bggcli.util.csvreader import CsvReader
from bggcli.ui.gamepage import GamePage
from bggcli.ui.loginpage import LoginPage
from bggcli.util.logger import Logger
from bggcli.util.webdriver import WebDriver


def execute(args, options):
    login = args['--login']

    file_path = check_file(args)

    csv_reader = CsvReader(file_path)
    csv_reader.open()

    game_count = csv_reader.rowCount

    if not args['--force']:
        sys.stdout.write(
            "You are about to delete %s games in you collection (%s), "
            "please enter the number of games displayed here to confirm you want to continue: "
            % (game_count, login))

        if raw_input() != game_count.__str__():
            Logger.error('Operation canceled, number does not match (should be %s).' % game_count,
                         sysexit=True)
            return

    Logger.info("Deleting games for '%s' account..." % login)

    with WebDriver('collection-delete', args, options) as web_driver:
        if not LoginPage(web_driver.driver).authenticate(login, args['--password']):
            sys.exit(1)

        Logger.info("Deleting %s games..." % game_count)
        game_page = GamePage(web_driver.driver)
        csv_reader.iterate(lambda row: game_page.delete(row))
        Logger.info("Deletion has finished.")
