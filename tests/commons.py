import os

LOGIN = os.environ.get('BGGCLI_TEST_LOGIN')
PASSWORD = os.environ.get('BGGCLI_TEST_PASSWORD')
COLLECTION_CSV_PATH = os.path.join(os.path.dirname(__file__), 'resources/collection.csv')
COLLECTION_XML_PATH = os.path.join(os.path.dirname(__file__), 'resources/collection.xml')
CSV_COLUMN_TO_IGNORE = ['language']


def debug_test(msg=""):
    print "[bggcli-test] %s" % msg
