import csv
from bggcli.commands import collection_export

from bggcli.main import _main
from bggcli.ui.collectionpage import CollectionPage
from bggcli.util.webdriver import WebDriver
from commons import *


def compare_csv_files(file_actual, file_expected):
    reader_actual = csv.DictReader(open(file_actual, 'rU'))
    reader_expected = csv.DictReader(open(file_expected, 'rU'))

    index = 1
    for row_actual in reader_actual:
        row_expected = reader_expected.next()
        for col in CSV_COLUMN_TO_IGNORE:
            del row_actual[col]
            del row_expected[col]
        assert row_actual == row_expected, \
            'Values are not the expected ones at line %s in %s!\n* Expected: %s\n* Actual: %s' \
            % (index, file_actual, row_expected, row_actual)
        index += 1

    try:
        reader_expected.next()
        assert False, "Expected file has more lines than the actual one!"
    except StopIteration:
        pass


def test_collection(tmpdir):
    """
    End-2-end test to verify collection-delete/export/import services
    """

    debug_test()
    debug_test("End-to-end test is executed in %s" % tmpdir)

    #
    debug_test()
    debug_test("1. Ensure the collection is empty")
    with WebDriver('test_collection-empty') as web_driver:
        if not CollectionPage(web_driver.driver).is_empty(LOGIN):
            try:
                _main(['-v', '--login', LOGIN, '--password', PASSWORD,
                      'collection-delete', '--force', COLLECTION_CSV_PATH])
            except BaseException as e:
                assert False, "Delete command should not fail: %s" % e

            assert CollectionPage(web_driver.driver).is_empty(LOGIN), 'Collection should be empty!'
            debug_test("-> [ok (collection was not empty)]")
        else:
            debug_test("-> [ok (collection was empty)]")

    debug_test()
    debug_test("2. Import collection")
    _main(['-v', '--login', LOGIN, '--password', PASSWORD,
          'collection-import', COLLECTION_CSV_PATH])
    debug_test("-> [ok]")

    #
    debug_test()
    debug_test("3. Export collection as CSV")
    actual_file = tmpdir.join('actual-collection.csv').strpath
    assert not os.path.exists(actual_file)
    _main(['-v', '--login', LOGIN, '--password', PASSWORD,
          'collection-export', actual_file])
    assert os.path.isfile(actual_file)
    debug_test("-> [ok]")

    #
    debug_test()
    debug_test("4. Compare CSV files")
    compare_csv_files(actual_file, COLLECTION_CSV_PATH)
    debug_test("Comparison OK!")

    debug_test()
    debug_test("End-to-end test on collection commands is successful!")


def test_export_xml_to_csv(tmpdir):
    generated_csv_file = tmpdir.join('xml-converted.csv').strpath
    collection_export.write_csv(COLLECTION_XML_PATH, generated_csv_file)
    compare_csv_files(generated_csv_file, COLLECTION_CSV_PATH)
