"""
bgg.logger
~~~~~~~~~~~~

Utility in charge of logging.

NB: we don't user the logging package since we want to narrow the scope (1 logger, only stdout,
no formatting) and possibly manage progress in some logs

"""
from __future__ import print_function
import sys
import traceback


class Logger(object):
    inlineMode = False
    isVerbose = False

    @staticmethod
    def error(msg, error=None, break_line=True, sysexit=False):
        if Logger.inlineMode:
            Logger.inlineMode = False
            print('')
        Logger._trace(sys.stderr, "ERROR: %s" % msg, False, break_line)
        if error is not None:
            # Avoid empty messages with some TimeoutExceptions
            if not str(error) or str(error).strip() == "Message:":
                error = "%s (no more details)" % repr(error)
            print("Cause: %s" % error, file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
        if sysexit:
            sys.exit(1)

    @staticmethod
    def info(msg, append=False, break_line=True):
        Logger.inlineMode = False
        Logger._trace(sys.stdout, msg, append, break_line)

    @staticmethod
    def verbose(msg, append=False, break_line=True):
        Logger.inlineMode = False
        if Logger.isVerbose:
            Logger._trace(sys.stdout, msg, append, break_line)

    @staticmethod
    def _trace(out, msg, append, break_line):
        if not append:
            msg = "[bggcli] %s" % msg
        if break_line:
            end = "\n"
        else:
            end = ""
        print(msg, file=out, end=end)
        out.flush()
