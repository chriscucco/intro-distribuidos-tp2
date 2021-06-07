import time


class Logger:
    def logIfVerbose(verbose, message):
        if verbose:
            print("Timestamp: " + str(time.time()) + "/ " + message)

    def logIfNotQuiet(quiet, message):
        if not quiet:
            print(message)

    def log(message):
        print(message)
