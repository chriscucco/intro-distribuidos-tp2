import os

from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.logger.logger import Logger
from lib.serverConnection.queueHandler import QueueHandler
import random


class ClientUpload:

    def __sendFile(s, host, port, file, fName, msgQueue, recvMsg,
                   verbose, quiet, lr):

        bytesSent = 0
        addr = (host, port)
        Logger.logIfNotQuiet(quiet, "Sending file to server...")
        endRecv = False
        while True:
            r = random.random()

            if r >= lr:
                file.seek(bytesSent, os.SEEK_SET)
                data = file.read(Constants.getMaxReadSize())

                if len(data) == 0:
                    Logger.logIfVerbose(verbose, "Sending EOF to server: "
                                        + str(host) + ", " + str(port))
                    msg = CommonConnection.sendEndFile(s, host, port,
                                                       fName, bytesSent)
                    msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr))
                    while not endRecv:
                        msgRcvd = CommonConnection.recvMsgFromServer(s, addr)
                        r = random.random()
                        if r >= lr:
                            recvMsg[msgRcvd+'-'+str(host)+'-'+str(port)] = True
                            if msgRcvd[0] == 'A' and msgRcvd[1] == 'E':
                                endRecv = True
                    break
                message = CommonConnection.sendMessage(s, host, port,
                                                       fName, data,
                                                       bytesSent)
                msgQueue.put(QueueHandler.makeMessageExpected(message, addr))

            msgRcvd = CommonConnection.recvMsgFromServer(s, addr)
            r = random.random()
            if r >= lr:
                recvMsg[msgRcvd+'-'+str(addr[0])+'-'+str(addr[1])] = True
                if msgRcvd[0] == Constants.errorProtocol():
                    Logger.log("Server cant process the file transfer")
                    CommonConnection.sendACK(s, host, port, 'F', fName,
                                             bytesSent)
                    file.close()
                    return False

                if msgRcvd[0] == Constants.ackProtocol():
                    splittedMsg = msgRcvd.split(';')
                    bytesSent = int(splittedMsg[1])
        return True

    def upload(self, sckt, host, port, file, fName, msgQueue, recvMsg,
               verbose, quiet, lr):

        Logger.logIfVerbose(verbose, "Sending upload code to server:" +
                            str(host) + ", " + str(port))
        message = Constants.uploadProtocol() + fName
        addr = (host, port)
        sckt.sendto(message.encode(), addr)
        msgQueue.put(QueueHandler.makeSimpleExpected(message.encode(), addr))

        message = CommonConnection.recvMsgFromServer(sckt, addr)
        recvMsg[message+'-'+str(addr[0])+'-'+str(addr[1])] = True

        transferOk = False

        if message[0] == Constants.ackProtocol():
            transferOk = ClientUpload.__sendFile(sckt, host, port, file, fName,
                                                 msgQueue, recvMsg, verbose,
                                                 quiet, lr)
        elif message[0] == Constants.errorProtocol():
            Logger.log("Server cant process upload work")
            CommonConnection.sendACK(sckt, host, port, 'F', fName, 0)
            file.close()
            return

        if transferOk:
            Logger.log("The transaction ended correctly")
            file.close()

        return
