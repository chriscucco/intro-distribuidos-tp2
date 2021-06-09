import sys
from lib.params.paramsValidation import Params
from lib.logger.logger import Logger
from lib.constants import Constants

DOWNLOAD_CLIENT_PARAMS = Constants.noValueCommands() + ['-H', '--host', '-p',
                                                        '--port', '-lr',
                                                        '--loss-rate', '-d',
                                                        '--dst', '-n',
                                                        '--name']


class DownloadClientParams(Params):
    def validate():
        host, port, verbose, quiet, helpParam, lossRate = Params.validate()
        fName, fDest = DownloadClientParams.getDestinationPathAndFilename()
        Logger.logIfVerbose(verbose, "Params parsed")
        return host, port, fName, fDest, verbose, quiet, helpParam, lossRate

    def getDestinationPathAndFilename():
        fName = ''
        fDest = ''
        i = 0
        commandWithValue = False

        while i < len(sys.argv):

            Params.validateCommand(DOWNLOAD_CLIENT_PARAMS, commandWithValue, i)

            if sys.argv[i] == '-d' or sys.argv[i] == '--dst':
                if len(sys.argv) > i+1:
                    fDest = sys.argv[i+1]
                    i += 1
            if sys.argv[i] == '-n' or sys.argv[i] == '--name':
                if len(sys.argv) > i+1:
                    fName = sys.argv[i+1]
                    i += 1

            commandWithValue = Params.commandHasValue(i)

            i += 1
        if fName == '':
            fName = 'test.txt'
        if fDest == '':
            fDest = './test.txt'
        return fName, fDest
