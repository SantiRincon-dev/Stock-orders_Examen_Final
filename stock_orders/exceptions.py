class InvalidPriceError(Exception):
    def __init__ (self, message):
           super().__init__(message)

class DuplicateOrderError(Exception):
    def __init__ (self, message):
           super().__init__(message)

class OrderNotFoundError(Exception):
    def __init__ (self, message):
           super().__init__(message)
