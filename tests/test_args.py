from docopt import DocoptExit
from bggcli.main import _main


def test_noarg(capsys):
    try:
        _main([])
        assert False, "Should have exited here!"
    except SystemExit as e:
        out, err = capsys.readouterr()

        assert not e.code
        assert "Usage:" in out
        assert "Available commands are:" in out


def test_help(capsys):
    try:
        _main(['help'])
        assert False, "Should have exited here!"
    except SystemExit as e:
        out, err = capsys.readouterr()

        assert not e.code
        assert "Usage:" in out
        assert "Available commands are:" in out


def test_help_command(capsys):
    try:
        _main(['help', 'collection-delete'])
        assert False, "Should have exited here!"
    except SystemExit as e:
        out, err = capsys.readouterr()

        assert not e.code
        assert "Usage:" in out
        assert "Available options:" not in out
        assert "Available commands are:" not in out
        assert "collection-delete" in out


def test_unknown_command(capsys):
    try:
        _main(['unknown'])
        assert False, "Should have exited here!"
    except SystemExit as e:
        out, err = capsys.readouterr()

        assert not e.code
        assert "Usage:" in out
        assert "Available commands are:" in out
        assert "Unknown command:" in err


def test_missing_option():
    try:
        # Miss password
        _main("-l mylogin collection-delete file1".split(" "))
        assert False, "Should have exited here!"
    except DocoptExit as e:
        # docopt breaks exit code management with its DocoptExit class
        assert "Usage:" in e.code
    except Exception as e:
        assert False, "Should have raised a DocoptExit and not %s" % e


def test_missing_arg():
    try:
        # Miss password
        _main("-l mylogin -p password collection-delete".split(" "))
        assert False, "Should have exited here!"
    except DocoptExit as e:
        # docopt breaks exit code management with its DocoptExit class
        assert "Usage:" in e.code
    except Exception as e:
        assert False, "Should have raised a DocoptExit and not %s" % e
