"""
bgg.csvreader
~~~~~~~~~~~~

Utility in charge of reading the CSV file

"""

import csv

from selenium.common.exceptions import WebDriverException

from bggcli import UI_ERROR_MSG, BGG_SUPPORTED_FIELDS
from bggcli.util.logger import Logger


class CsvReader:
    reader = None

    def __init__(self, file_path):
        self.file = open(file_path, 'rU')
        self.rowCount = 0

    @staticmethod
    def count_lines(f):
        count = 0
        tmp_reader = csv.DictReader(f)
        for _ in tmp_reader:
            count += 1
        f.seek(0)
        return count

    def open(self):
        self.rowCount = self.count_lines(self.file)
        self.reader = csv.DictReader(self.file)
        self.check()

    def iterate(self, callback):
        try:
            index = 1
            for row in self.reader:
                objectid = row.get('objectid')
                if objectid is None or not objectid.isdigit():
                    Logger.error("No valid 'objectid' at line %s!" % index, None, sysexit=True)
                    return

                # Encode in UTF-8
                for key in row:
                    value = row[key]
                    if value is not None:
                        row[key] = unicode(value, 'utf-8')

                objectname = row['objectname']
                if objectname is None or objectname == "":
                    objectname = "(name not available for objectid=%s)" % objectid

                Logger.info("[%s/%s] %s... " % (index, self.rowCount, objectname),
                            break_line=False)
                try:
                    callback(row)
                except WebDriverException as e:
                    Logger.error(UI_ERROR_MSG, e, sysexit=True)
                    return
                except Exception as e:
                    Logger.info("", append=True)
                    Logger.error("Unexpected error while processing row %s" % index, e,
                                 sysexit=True)
                    return
                Logger.info(" [done]", append=True)
                index += 1
        except csv.Error as e:
            Logger.error('Error while reading file %s at line %d: %s'
                         % (file, self.reader.line_num, e), sysexit=True)

    def check(self):
        if 'objectid' not in self.reader.fieldnames:
            Logger.error("Cannot process the CSV file, it should contain at least a column named "
                         "'objectid'! Provided columns: %s" % self.reader.fieldnames, sysexit=True)
            return

        unknown_fields = set(self.reader.fieldnames) - set(BGG_SUPPORTED_FIELDS)
        if unknown_fields:
            Logger.info('Some fields are not supported in your CSV file, they will be skipped: %s'
                        % unknown_fields)

    def __del__(self):
        self.file.close()
