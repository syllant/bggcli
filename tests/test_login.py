from bggcli.main import _main
from commons import *


def test_invalid_login(capsys):
    debug_test()
    debug_test("Test a failed authentication...")

    try:
        _main(("-l bggcli -p fake collection-import %s" % COLLECTION_CSV_PATH).split(" "))
    except SystemExit as e:
        out, err = capsys.readouterr()

        assert e.code == 1
        assert "Authenticating" in out
        assert "Authentication failed" in err
        debug_test()
        debug_test("Failed authentication test is OK!")
