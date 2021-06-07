import datetime


class Logger:
    def logIfVerbose(verbose, message):
        if verbose:
            print(str(datetime.datetime.now()) + ": " + message)

    def logIfNotQuiet(quiet, message):
        if not quiet:
            print(message)

    def log(message):
        print(message)
