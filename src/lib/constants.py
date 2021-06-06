
DATA_CHUNK = 1024
MAX_READ_SIZE = 980
TTL = 0.5
MAX_HEADER_TRANS_PROTOCOL_SIZE = 44
DOWNLOAD = "D"
UPLOAD = "U"
TRANSFER = "T"
ACK = "A"
END = "E"
ERROR = "F"
NO_VALUE_COMMANDS = ['-h', '--help', '-v', '--verbose', '-q', '--quiet']


class Constants:

    def bytesChunk():
        return DATA_CHUNK

    def getMaxReadSize():
        return MAX_READ_SIZE

    def uploadProtocol():
        return UPLOAD

    def downloadProtocol():
        return DOWNLOAD

    def fileTransferProtocol():
        return TRANSFER

    def ackProtocol():
        return ACK

    def errorProtocol():
        return ERROR

    def endProtocol():
        return END

    def ttl():
        return TTL

    def maxHeaderTransProtocolSize():
        return MAX_HEADER_TRANS_PROTOCOL_SIZE

    def noValueCommands():
        return NO_VALUE_COMMANDS
