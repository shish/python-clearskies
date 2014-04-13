class ClientException(Exception):
    pass


class TransportException(ClientException):
    pass


class ProtocolException(ClientException):
    pass
