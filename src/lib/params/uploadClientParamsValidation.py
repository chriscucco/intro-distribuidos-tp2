import sys
from lib.params.paramsValidation import Params
from lib.logger.logger import Logger
from lib.constants import Constants

UPLOAD_CLIENT_PARAMS = Constants.noValueCommands() + ['-H', '--host', '-p',
                                                      '--port', '-lr',
                                                      '--loss-rate', '-s',
                                                      '--src', '-n', '--name']


class UploadClientParams(Params):
    def validate():
        host, port, verbose, quiet, helpParam, lr = Params.validate()
        fName, fSourcePath = UploadClientParams.getSourcePathAndFilename()
        Logger.logIfVerbose(verbose, "Params parsed")
        return host, port, fName, fSourcePath, verbose, quiet, helpParam, lr

    def getSourcePathAndFilename():
        fName = ''
        fSourcePath = ''
        i = 0
        commandWithValue = False

        while i < len(sys.argv):

            Params.validateCommand(UPLOAD_CLIENT_PARAMS, commandWithValue, i)

            if sys.argv[i] == '-s' or sys.argv[i] == '--src':
                if len(sys.argv) > i+1:
                    fSourcePath = sys.argv[i+1]
                    i += 1

            if sys.argv[i] == '-n' or sys.argv[i] == '--name':
                if len(sys.argv) > i+1:
                    fName = sys.argv[i+1]
                    i += 1

            commandWithValue = Params.commandHasValue(i)

            i += 1
        if fName == '':
            fName = 'test.txt'
        if fSourcePath == '':
            fSourcePath = './test.txt'
        return fName, fSourcePath
