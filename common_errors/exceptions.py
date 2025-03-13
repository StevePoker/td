class MissedParam(Exception):
    def __init__(self, message):
        super().__init__(message)


class UnexpectedParam(Exception):
    def __init__(self, message):
        super().__init__(message)


class TooManyParams(Exception):
    def __init__(self, message):
        super().__init__(message)
