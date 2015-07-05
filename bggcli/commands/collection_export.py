"""
Export a game collection as a CSV file.

Usage: bggcli [-v] -l <login> -p <password>
              [-c <name>=<value>]...
              collection-export <file>

Options:
    -v                              Activate verbose logging
    -l, --login <login>             Your login on BGG
    -p, --password <password>       Your password on BGG
    -c <name=value>                 To specify advanced options, see below

Advanced options:
    save-xml-file=<true|false>      To store the exported raw XML file in addition (will be
                                    save aside the CSV file, with '.xml' extension
    browser-keep=<true|false>       If you want to keep your web browser opened at the end of the
                                    operation
    browser-profile-dir=<dir>       Path or your browser profile if you want to use an existing

Arguments:
    <file> The CSV file to generate
"""
import csv
import urllib2
import time
import sys
import xml.etree.ElementTree as ET

from bggcli import BGG_BASE_URL, BGG_SUPPORTED_FIELDS
from bggcli.ui.loginpage import LoginPage
from bggcli.util.logger import Logger
from bggcli.util.webdriver import WebDriver
from bggcli.util.xmltocsv import XmlToCsv

BGG_SESSION_COOKIE_NAME = 'SessionID'
EXPORT_QUERY_INTERVAL = 5
ERROR_FILE_PATH = 'error.txt'


def execute(args, options):
    login = args['--login']
    dest_path = args['<file>']

    Logger.info("Exporting collection for '%s' account..." % login)

    # 1. Authentication
    with WebDriver('collection-export', args, options) as web_driver:
        if not LoginPage(web_driver.driver).authenticate(login, args['--password']):
            sys.exit(1)
        auth_cookie = web_driver.driver.get_cookie(BGG_SESSION_COOKIE_NAME)['value']

    # 2. Export
    # Easier to rely on a client HTTP call rather than Selenium to download a file
    # Just need to pass the session cookie to get the full export with private information

    # Use XML2 API, see https://www.boardgamegeek.com/wiki/page/BGG_XML_API2#Collection
    # Default CSV export doesn't provide version info!
    url = '%s/xmlapi2/collection?username=%s&version=1&showprivate=1&stats=1' \
          % (BGG_BASE_URL, login)
    req = urllib2.Request(url, None, {'Cookie': '%s=%s' % (BGG_SESSION_COOKIE_NAME, auth_cookie)})

    # Get a BadStatusLine error most of times without this delay!
    # Related to Selenium, but in some conditions that I have not identified
    time.sleep(8)
    try:
        Logger.info('Launching export...')
        response = default_export(req)
    except Exception as e:
        Logger.error('Error while fetching export file!', e, sysexit=True)
        return

    # 3. Store XML file if requested
    xml_file = options.get('save-xml-file')
    if xml_file == 'true':
        xml_file_path = write_xml_file(response, dest_path)
        Logger.info("XML file save as %s" % xml_file_path)
        source = open(xml_file_path, 'rU')
    else:
        source = response

    # 4. Write CSV file
    try:
        write_csv(source, dest_path)
    except Exception as e:
        Logger.error('Error while writing export file in file system!', e, sysexit=True)
        return
    finally:
        source.close()

    # End
    Logger.info("Collection has been exported as %s" % dest_path)


def default_export(req):
    response = urllib2.urlopen(req)

    if response.code == 202:
        Logger.info('Export is queued, will retry in %ss' % EXPORT_QUERY_INTERVAL)
        time.sleep(EXPORT_QUERY_INTERVAL)
        return default_export(req)

    if response.code == 200:
        return response

    # Write response in a text file otherwise
    try:
        with open(ERROR_FILE_PATH, "wb") as error_file:
            error_file.write(response.read())
        Logger.error("Unexpected response, content has been written in %s" % ERROR_FILE_PATH)
    except Exception as e:
        raise Exception('Unexpected HTTP response for export request, and cannot write '
                        'response content in %s: %s' % (ERROR_FILE_PATH, e))
    raise Exception('Unexpected HTTP response for export request, response content written in '
                    '%s' % ERROR_FILE_PATH)


def write_xml_file(response, csv_dest_path):
    dest_path = '.'.join(csv_dest_path.split('.')[:-1]) + '.xml'
    with open(dest_path, "wb") as dest_file:
        dest_file.write(response.read())

    return dest_path


def write_csv(source, dest_path):
    with open(dest_path, "wb") as dest_file:
        csv_writer = csv.DictWriter(dest_file, fieldnames=BGG_SUPPORTED_FIELDS,
                                    quoting=csv.QUOTE_ALL)
        # csv_writer.writeheader() use quotes
        dest_file.write('%s\n' % ','.join(BGG_SUPPORTED_FIELDS))

        for event, elem in ET.iterparse(source, events=['end']):
            if event == 'end':
                if elem.tag == 'item' and elem.attrib.get('subtype') == 'boardgame':
                    row = XmlToCsv.convert_item(elem)
                    csv_writer.writerow(row)

