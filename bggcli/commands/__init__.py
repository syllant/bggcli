import os

from bggcli.util.logger import Logger


def check_file(args):
    file_path = args['<file>']

    if os.path.isfile(file_path):
        return file_path

    Logger.error("File does not exist: %s" % file_path, sysexit=True)
