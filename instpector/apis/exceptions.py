class InstpectorException(Exception):
    pass

class AuthenticateFailException(InstpectorException):
    pass

class AuthenticateRevokeException(InstpectorException):
    pass

class ParseDataException(InstpectorException):
    pass

class NotImplementedException(InstpectorException):
    pass

class NoDataException(InstpectorException):
    pass
