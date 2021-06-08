import socket
import queue
import datetime
from threading import Thread
from lib.params.uploadClientParamsValidation import UploadClientParams
from lib.logger.logger import Logger
from lib.clientConnection.clientUpload import ClientUpload
from lib.serverConnection.queueHandler import QueueHandler
from lib.exceptions.paramException import ParamException


def main():
    startTime = datetime.datetime.now()
    host, port, fName, fSource, v, q, h, lr = '', '', '', '', '', '', '', ''
    try:
        host, port, fName, fSource, v, q, h, lr = UploadClientParams.validate()
    except ParamException as e:
        Logger.log(e.message)
        printHelp()
        return

    if h:
        return printHelp()

    try:
        Logger.logIfVerbose(v, 'Opening file: ' + fName)
        file = open(fSource + fName, "rb")
    except OSError:
        Logger.log("Error opening file " + fSource + fName)
        return

    sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Logger.logIfVerbose(v, "Creating socket...")

    msgQueue = queue.Queue()
    recvMsg = {}
    queueThread = Thread(target=runQueue, args=(sckt, msgQueue, recvMsg, v))
    queueThread.start()

    clientUpload = ClientUpload()

    clientUpload.upload(sckt, host, port, file, fName, msgQueue, recvMsg,
                        v, q, lr)

    # Se cierra cliente
    msgQueue.put('exit')
    queueThread.join()
    sckt.close()
    Logger.logIfNotQuiet(q, "Client closed")
    endTime = datetime.datetime.now()
    executionTime = (endTime - startTime).total_seconds() * 1000.0
    Logger.log('Execution time: ' + str(int(executionTime)) + 'ms')
    return


def printHelp():
    print('usage: upload-file.py [-h] [-v|-q] [-H ADDR] [-p PORT]')
    print('[-s FILEPATH] [-n FILENAME] [-lr LOSSRATE]')
    print('')
    print('<command description>')
    print('')
    print('optional arguments:')
    print('-h, --help           show this help message and exit')
    print('-v, --verbose        increase output verbosity')
    print('-q, --quiet          decrease output verbosity')
    print('-H, --host           server IP address')
    print('-p, --port           server port')
    print('-s, --src            source file path')
    print('-n, --name           file name')
    print('-lr, --loss-rate     loss messages rate (value between 0 and 0.99)')


def runQueue(skt, msgQueue, recvMsg, v):
    QueueHandler.handleQueue(skt, msgQueue, recvMsg, v)
    return


if __name__ == "__main__":
    main()
