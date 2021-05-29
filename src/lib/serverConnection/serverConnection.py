from lib.constants import Constants
from lib.commonConnection.commonConnection import CommonConnection
from lib.logger.logger import Logger
from lib.helpers.fileHelper import FileHelper
from lib.serverConnection.queueHandler import QueueHandler
import random
import os


class Connection:
    def startCommunicating(s, fs, sPath, queue, recvMsg, v, q, lr):
        try:
            while True:
                r = random.random()
                data, addr = s.recvfrom(Constants.bytesChunk())
                if r > lr:
                    Logger.logIfVerbose(v, "Recieved message from: " + str(addr))
                    mode = data[0:1]
                    if mode.decode() == 'A':
                        msg = data.decode()
                        qMsg = msg + '-' + str(addr[0]) + '-' + str(addr[1])
                        recvMsg[qMsg] = True
                    Connection.process(s, fs, data, addr, sPath, queue, v, q)
            return
        except Exception as e:
            Logger.log(e)
            return

    def process(s, f, msg, addr, pth, queue, v, q):
        mode = msg[0:1].decode()
        data = msg[1:]
        if mode == Constants.uploadProtocol():
            Connection.startUpload(s, f, data, addr, pth, queue, v, q)
        elif mode == Constants.downloadProtocol():
            Connection.startDownload(s, f, data, addr, pth, queue, v, q)
        elif mode == Constants.errorProtocol():
            Connection.processError(s, f, data, addr, v, q)
        elif mode == Constants.endProtocol():
            Connection.processEnd(s, f, data, addr, v, q)
        elif mode == Constants.ackProtocol():
            Connection.processAck(s, f, data, addr, queue, v, q)
        elif mode == Constants.fileTransferProtocol():
            Connection.processTransfer(s, f, data, addr, queue, v, q)
        return

    def startUpload(s, files, msg, addr, sPath, msgQueue, verbose, quiet):
        message = msg.decode()
        try:
            file = open(sPath+message, "wb")
            Logger.logIfVerbose(verbose, "File " + message + " opened")
            files[message] = file
            Logger.logIfVerbose(verbose, "Sending ACK to client: " + str(addr))
            CommonConnection.sendACK(s, addr[0], addr[1], 'U', message, 0)
        except OSError:
            Logger.log(quiet, "Error opening file " + message)
            msg = CommonConnection.sendError(s, message, addr[0], addr[1])
            msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr))
            return
        return

    def processTransfer(s, files, data, addr, msgQueue, v, q):
        values = data[0: Constants.maxHeaderTransProtocolSize() - 1].decode()
        separatorPossition = values.find(';')
        fname = values[0:separatorPossition]
        processedData = values[separatorPossition+1:]
        separatorPossition = processedData.find(';')
        bytesRecv = int(processedData[0:separatorPossition])
        msg = data[Constants.maxHeaderTransProtocolSize() - 1:]
        try:
            f = files[fname]
            Connection.upload(s, f, fname, bytesRecv, msg, addr, v, q)
        except Exception as e:
            print(e)
            Logger.logIfNotQuiet(q, "Error processing transfer")
            msg = CommonConnection.sendError(s, fname, addr[0], addr[1])
            msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr))
        return

    def startDownload(s, files, data, addr, sPath, msgQueue, v, q):
        filename = data.decode()
        try:
            file = open(sPath+filename, "rb")
            files[filename] = file
            data = file.read(Constants.getMaxReadSize())
            h = addr[0]
            p = addr[1]
            Logger.logIfVerbose(v, "Sending message to client: " + str(addr))
            msg = CommonConnection.sendMessage(s, h, p, filename, data, 0)
            msgQueue.put(QueueHandler.makeMessageExpected(msg, addr))
        except Exception:
            Logger.log(q, "Error opening file " + filename)
            msg = CommonConnection.sendError(s, filename, addr[0], addr[1])
            msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr))
            return
        return

    def processError(s, files, data, addr, v, q):
        filename = data.decode()
        try:
            files[filename].close()
            Logger.logIfVerbose(v, "Sending ACK to client: " + str(addr))
            CommonConnection.sendACK(s, addr[0], addr[1], 'F', filename, 0)
        except Exception:
            Logger.log(q, "Error processing error")
            return
        return

    def processEnd(s, files, data, addr, v, q):
        filename = data.decode()
        try:
            files[filename].close()
            Logger.logIfVerbose(v, "Sending ACK to client: " + str(addr))
            CommonConnection.sendACK(s, addr[0], addr[1], 'E', filename, 0)
        except Exception:
            Logger.log(q, "Error processing end file")
            return
        return

    def processAck(s, files, msg, addr, queue, v, q):
        data = msg.decode()
        md = data[0]
        processedData = data[1:]
        if md == Constants.endProtocol() or md == Constants.errorProtocol():
            return
        elif md == Constants.fileTransferProtocol():
            separatorPossition = processedData.find(';')
            fname = processedData[0:separatorPossition]
            bRecv = int(processedData[separatorPossition+1:])
            f = files[fname]
            return Connection.download(s, f, fname, bRecv, addr, queue, v, q)
        return

    def download(s, f, fname, br, addr, msgQueue, v, q):
        f.seek(br, os.SEEK_SET)
        Logger.logIfVerbose(v, "Reading file " + fname)
        data = f.read(Constants.getMaxReadSize())
        if len(data) == 0:
            Logger.logIfVerbose(v, "Sending EndFile to client: " + str(addr))
            msg = CommonConnection.sendEndFile(s, addr[0], addr[1], fname, 0)
            msgQueue.put(QueueHandler.makeSimpleExpected(msg, addr))
        else:
            h = addr[0]
            port = addr[1]
            Logger.logIfVerbose(v, "Sending message to client: " + str(addr))
            msg = CommonConnection.sendMessage(s, h, port, fname, data, br)
            msgQueue.put(QueueHandler.makeMessageExpected(msg, addr))
        return

    def upload(s, f, fname, bytesRecv, msg, addr, v, q):
        f.seek(bytesRecv, os.SEEK_SET)
        Logger.logIfVerbose(v, "Writing file " + fname)
        f.write(msg)
        filesize = FileHelper.getFileSize(f)
        Logger.logIfVerbose(v, "Sending ACK to client: " + str(addr))
        CommonConnection.sendACK(s, addr[0], addr[1], 'T', fname, filesize)
        return
