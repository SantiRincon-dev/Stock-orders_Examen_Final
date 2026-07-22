from stock_orders.exceptions import InvalidPriceError
from abc import ABC, abstractmethod


class Stock:
    def __init__(self, symbol: str, company: str, price: float) -> None:
        self.symbol = symbol
        self.company = company
        self.__price = price

    def get_price(self) -> float:
        return self.__price

    def set_price(self, value: float) -> None:
        if value <= 0:
            raise InvalidPriceError(
                f"El precio de {self.symbol} no puede ser menor o igual a 0."
            )
        self.__price = value


class Transaction:
    def __init__(
        self,
        buy_order: "BuyOrder",
        sell_order: "SellOrder",
        quantity: int,
        price: float,
    ) -> None:
        self.buy_order = buy_order
        self.sell_order = sell_order
        self.quantity = quantity
        self.price = price

    def get_summary(self) -> str:
        return (
            f"Transacción exitosa: {self.quantity} "
            f"{self.buy_order.symbol} a $ {self.price}"
        )

class Order(ABC):
    """Clase base abstracta para las órdenes de compra y venta."""

    _counter = 0  # el contador lo van a compartir Order, BuyOrder y SellOrder

    def __init__(
        self, order_id: str, trader: str, symbol: str, quantity: int, price: float
    ) -> None:
        self.order_id = order_id
        self.trader = trader
        self.symbol = symbol
        self.quantity = quantity
        self.price = price
        self.is_cancelled = False

        self._seq = Order._counter
        Order._counter += 1

    @abstractmethod
    def execute(self) -> str:
        raise NotImplementedError

    def get_summary(self) -> str:
        estado = "CANCELADA" if self.is_cancelled else "ACTIVA"
        return (
            f"[{self.order_id}] {type(self).__name__} - {self.trader} - "
            f"{self.symbol} x{self.quantity} @ ${self.price} ({estado})"
        )


class BuyOrder(Order):
    def execute(self) -> str:
        return (
            f"Orden de COMPRA {self.order_id} ejecutada: "
            f"{self.trader} compra {self.quantity} {self.symbol} @ ${self.price}"
        )


class SellOrder(Order):
    def execute(self) -> str:
        return (
            f"Orden de VENTA {self.order_id} ejecutada: "
            f"{self.trader} vende {self.quantity} {self.symbol} @ ${self.price}"
        )
