import datetime

DATETIME = str(datetime.datetime.now()) + ": "


class Logger:
    def logIfVerbose(verbose, message):
        if verbose:
            print(DATETIME + message)

    def logIfNotQuiet(quiet, message):
        if not quiet:
            print(DATETIME + message)

    def log(message):
        print(DATETIME + message)
