class LibreScoreException(Exception):
    pass

class ScoreNotFoundException(LibreScoreException):
    pass

class AuthenticationException(LibreScoreException):
    pass

class DownloadException(LibreScoreException):
    pass