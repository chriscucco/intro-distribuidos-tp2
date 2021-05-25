import os
from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.helpers.fileHelper import FileHelper
from lib.logger.logger import Logger
from lib.serverConnection.queueHandler import QueueHandler


class ClientDownload:
    def download(self, s, host, port, fName, fDest, msgQueue, recvMsg, v, q):
        message = Constants.downloadProtocol() + fName
        Logger.logIfVerbose(v, "Sending download request to server")
        addr = (host, port)
        s.sendto(message.encode(), addr)
        expected = QueueHandler.makeSimpleExpected(message.encode(), addr)
        msgQueue.put(expected)
        data, addr = s.recvfrom(Constants.bytesChunk())
        recvMsg[expected['expected']] = True
        mode = data[0:1]
        processedData = data[1:]
        file = self.processInitialMsg(s, fName, fDest, mode.decode(),
                                      addr, v, q)
        if file is None:
            return

        while True:
            if mode.decode() == Constants.fileTransferProtocol():
                values = processedData[0:43].decode()
                msg = processedData[43:]
                separatorPossition = values.find(';')
                fname = values[0:separatorPossition]
                processedData = values[separatorPossition+1:]
                separatorPossition = processedData.find(';')
                bRecv = int(processedData[0:separatorPossition])
                Logger.logIfVerbose(v, "Recieved " + str(bRecv) +
                                    " bytes from server: " + str(addr))
                file.seek(bRecv, os.SEEK_SET)
                file.write(msg)
                fileSize = FileHelper.getFileSize(file)
                Logger.logIfVerbose(v, "Sending ACK-T to server: "
                                    + str(addr))
                CommonConnection.sendACK(s, host, port, 'T',
                                         fname, fileSize)
            elif mode.decode() == Constants.endProtocol():
                Logger.logIfVerbose(v, "Sending ACK-E to server: "
                                    + str(addr))
                CommonConnection.sendACK(s, host, port, 'E', fname, 0)
                Logger.log("File downloaded successfully in: " + fDest + fname)
                file.close()
                return
            data, addr = s.recvfrom(Constants.bytesChunk())
            mode = data[0:1]
            processedData = data[1:]
        return

    def processInitialMsg(self, downSock, fName, fDest, mode,
                          addr, verb, quiet):
        if mode == Constants.errorProtocol():
            Logger.log("The file does not exist on the server")
            Logger.logIfVerbose(verb, "Sending ACK-F to server: " + str(addr))
            CommonConnection.sendACK(downSock, addr[0], addr[1], 'F', fName, 0)
            return None
        elif mode == Constants.fileTransferProtocol():
            try:
                file = open(fDest + fName, "wb")
                Logger.logIfVerbose(verb, "File created on client")
                return file
            except OSError:
                Logger.log("Client could not create the file on: "
                           + fDest + fName)
                return None
