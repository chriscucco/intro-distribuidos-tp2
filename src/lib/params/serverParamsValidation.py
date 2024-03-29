import sys
from lib.params.paramsValidation import Params
from lib.logger.logger import Logger
from lib.constants import Constants


SERVER_COMMANDS = Constants.noValueCommands() + ['-H', '--host', '-p',
                                                 '--port', '-lr',
                                                 '--loss-rate', '-s',
                                                 '--storage']


class ServerParams(Params):
    def validate():
        host, port, verbose, quiet, helpParam, lossRate = Params.validate()
        sPath = ServerParams.getStoragePath()
        Logger.logIfVerbose(verbose, "Params parsed")
        return host, port, sPath, verbose, quiet, helpParam, lossRate

    def getStoragePath():
        sPath = ''
        i = 0
        commandWithValue = False

        while i < len(sys.argv):

            Params.validateCommand(SERVER_COMMANDS, commandWithValue, i)

            if sys.argv[i] == '-s' or sys.argv[i] == '--storage':
                if len(sys.argv) > i+1:
                    sPath = sys.argv[i+1]
                    i += 1

            commandWithValue = Params.commandHasValue(i)

            i += 1
        if sPath == '':
            sPath = 'lib/'
        if sPath[-1] != '/':
            sPath += '/'
        return sPath
