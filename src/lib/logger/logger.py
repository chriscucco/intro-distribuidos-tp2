import datetime


class Logger:
    def logIfVerbose(verbose, message):
        if verbose:
            print(str(datetime.datetime.now()) + ": " + message)

    def logIfNotQuiet(quiet, message):
        if not quiet:
            print(str(datetime.datetime.now()) + ": " + message)

    def log(message):
        print(str(datetime.datetime.now()) + ": " + message)
