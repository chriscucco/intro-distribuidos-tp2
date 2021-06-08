from lib.params.serverParamsValidation import ServerParams
from lib.serverConnection.serverConnection import Connection
from lib.serverConnection.queueHandler import QueueHandler
from lib.logger.logger import Logger
from lib.exceptions.paramException import ParamException
from threading import Thread
import socket
import queue


def main():

    host, port, sPath, v, q, helpParam, lr = '', '', '', '', '', '', ''

    try:
        host, port, sPath, v, q, helpParam, lr = ServerParams.validate()
    except ParamException as e:
        printHelp()
        Logger.log(e.message)
        return

    if helpParam:
        return printHelp()

    Logger.log("Server started in host: " + host + " and port: " + str(port))

    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Logger.logIfNotQuiet(q, "Server socket successfully created")

    try:
        skt.bind((host, port))
        Logger.logIfVerbose(v, "Server socket binded")
    except socket.error:
        Logger.log("Error binding socket")
        return

    files = {}

    msgQueue = queue.Queue()
    rMsg = {}
    cont = {}
    queueThread = Thread(target=runQueue, args=(skt, msgQueue, rMsg, v))
    t = Thread(target=run, args=(skt, files, sPath, msgQueue, rMsg,
                                 cont, v, q, lr))
    t.start()
    queueThread.start()

    serverOn = True
    while serverOn:
        value = input()
        if value == 'exit':
            cont['exit'] = True
            serverOn = False

    Logger.logIfNotQuiet(q, "Closing server...")
    msgQueue.put('exit')
    t.join()
    queueThread.join()
    skt.close()

    for key, f in files.items():
        try:
            f.close
            Logger.logIfVerbose(v, "File " + key + " closed")
        except Exception:
            Logger.logIfNotQuiet(q, "Error closing file: " + key)
    Logger.log('Server closed')
    return


def run(s, f, sPath, msgQueue, recvMsg, cont, v, q, lr):
    Connection.startCommunicating(s, f, sPath, msgQueue, recvMsg,
                                  cont, v, q, lr)
    return


def runQueue(skt, msgQueue, recvMsg, v):
    QueueHandler.handleQueue(skt, msgQueue, recvMsg, v)
    return


def printHelp():
    print('usage: start-server.py [-h] [-v|-q] [-H ADDR] [-p PORT]')
    print(' [-s DIRPATH] [-lr LOSSRATE]')
    print('')
    print('<command description>')
    print('')
    print('optional arguments:')
    print('-h, --help           show this help message and exit')
    print('-v, --verbose        increase output verbosity')
    print('-q, --quiet          decrease output verbosity')
    print('-H, --host           service IP address')
    print('-p, --port           service port')
    print('-s, --storage        storage dir path')
    print('-lr, --loss-rate     loss messages rate (value between 0 and 1)')


if __name__ == "__main__":
    main()
