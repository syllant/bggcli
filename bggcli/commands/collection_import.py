"""
Import a game collection from a CSV file.

Note this action can be used to initialize a new collection, but also to update an existing
collection. Only the fields defined in the file will be updated.

Usage: bggcli [-v] -l <login> -p <password>
              [-c <name>=<value>]...
              collection-import <file>

Options:
    -v                              Activate verbose logging
    -l, --login <login>             Your login on BGG
    -p, --password <password>       Your password on BGG
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
from bggcli.ui.gamepage import GamePage
from bggcli.ui.loginpage import LoginPage
from bggcli.util.csvreader import CsvReader
from bggcli.util.logger import Logger
from bggcli.util.webdriver import WebDriver


def execute(args, options):
    login = args['--login']

    file_path = check_file(args)

    csv_reader = CsvReader(file_path)
    csv_reader.open()

    Logger.info("Importing games for '%s' account..." % login)

    with WebDriver('collection-import', args, options) as web_driver:
        if not LoginPage(web_driver.driver).authenticate(login, args['--password']):
            sys.exit(1)

        Logger.info("Importing %s games..." % csv_reader.rowCount)
        game_page = GamePage(web_driver.driver)
        csv_reader.iterate(lambda row: game_page.update(row))
        Logger.info("Import has finished.")
