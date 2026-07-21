from stock_orders.exceptions import InvalidPriceError
from abc import ABC

class Stock:
    def __init__(self, symbol: str, company: str, price: float) -> None:
        self.symbol = symbol
        self.company = company
        self.__price = price

    def get_price(self) -> float:
        return self.__price

    def set_price(self, value: float) -> None:
        if value <= 0:
            raise InvalidPriceError(f"El precio de {self.symbol} no puede ser menor o igual a 0.")
        self.__price = value

class Transaction:
    def __init__(self, buy_order: bool, sell_order: bool, quantity: int, price: float) -> None:
        self.buy_order = buy_order
        self.sell_order = sell_order
        self.quantity = quantity
        self.price = price
    
    def __str__(self):
        return f"Transacción exitosa: {self.quantity} {self.buy_order.symbol} a $ {self.price}"


