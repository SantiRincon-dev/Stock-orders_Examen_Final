from stock_orders.models import Stock, BuyOrder, SellOrder
from stock_orders.engine import ExchangeEngine
from stock_orders.exceptions import (
    DuplicateOrderError,
    InvalidPriceError,
    OrderNotFoundError,
)


if __name__ == "__main__":

    engine = ExchangeEngine()

    aapl = Stock("AAPL", "Apple", 190.0)
    tsla = Stock("TSLA", "Tesla", 220.0)

    b1 = BuyOrder("B1", "Ana", "AAPL", 10, 190.0)
    s1 = SellOrder("S1", "Luis", "AAPL", 10, 190.0)

    b2 = BuyOrder("B2", "Maria", "TSLA", 5, 210.0)
    s2 = SellOrder("S2", "Pedro", "TSLA", 5, 225.0)

    b3 = BuyOrder("B3", "Carlos", "AAPL", 10, 195.0)

    b4 = BuyOrder("B4", "Sofia", "TSLA", 5, 230.0)

    engine.place_order(b1)
    engine.place_order(s1)
    engine.place_order(b2)
    engine.place_order(s2)
    engine.place_order(b3)
    engine.place_order(b4)

    print("\n--- Cancelación válida ---")
    engine.cancel_order("B4")
    print(b4.get_summary())

    print("\n--- Match de órdenes ---")
    for transaction in engine.match_orders():
        print(transaction.get_summary())

    print("\n--- Órdenes pendientes ---")
    print(b1.get_summary())
    print(b2.get_summary())
    print(s2.get_summary())

    print("\n--- Orden duplicada ---")
    try:
        engine.place_order(
            BuyOrder("B1", "Juan", "AAPL", 2, 195.0)
        )
    except DuplicateOrderError as e:
        print(e)

    print("\n--- Precio inválido ---")
    try:
        aapl.set_price(-10)
    except InvalidPriceError as e:
        print(e)

    print("\n--- Orden inexistente ---")
    try:
        engine.cancel_order("B999")
    except OrderNotFoundError as e:
        print(e)

    print("\n--- Historial de transacciones ---")
    for transaction in engine.transactions():
        print(transaction.get_summary())