import heapq

from stock_orders.exceptions import DuplicateOrderError, OrderNotFoundError
from stock_orders.models import BuyOrder, SellOrder, Transaction


class ExchangeEngine:
    def __init__(self) -> None:
        self._buy_heaps = {}  # symbol -> list[tuple(-price, seq, order)]
        self._sell_heaps = {}  # symbol -> list[tuple(price, seq, order)]
        self._orders_by_id = {}  # order_id -> Order
        self._transactions = []  # list[Transaction], historial ya ejecutado

    def place_order(self, order) -> None:

        if order.order_id in self._orders_by_id:
            raise DuplicateOrderError(
                f"Ya existe una orden registrada con order_id '{order.order_id}'."
            )

        self._orders_by_id[order.order_id] = order

        if order.symbol not in self._buy_heaps:
            self._buy_heaps[order.symbol] = []
            self._sell_heaps[order.symbol] = []

        if isinstance(order, BuyOrder):
            heapq.heappush(
                self._buy_heaps[order.symbol], (-order.price, order._seq, order)
            )
        elif isinstance(order, SellOrder):
            heapq.heappush(
                self._sell_heaps[order.symbol], (order.price, order._seq, order)
            )

    def cancel_order(self, order_id: str) -> None:

        order = self._orders_by_id.get(order_id)
        if order is None:
            raise OrderNotFoundError(
                f"No existe una orden registrada con order_id '{order_id}'."
            )
        order.is_cancelled = True

    def match_orders(self):

        for symbol in self._buy_heaps:
            buy_heap = self._buy_heaps[symbol]
            sell_heap = self._sell_heaps[symbol]

            while buy_heap and sell_heap:
                # descartar canceladas en el tope de cada heap
                while buy_heap and buy_heap[0][2].is_cancelled:
                    heapq.heappop(buy_heap)
                while sell_heap and sell_heap[0][2].is_cancelled:
                    heapq.heappop(sell_heap)

                if not buy_heap or not sell_heap:
                    break

                neg_buy_price, buy_seq, buy_order = buy_heap[0]
                sell_price, sell_seq, sell_order = sell_heap[0]
                buy_price = -neg_buy_price

                if buy_price < sell_price:
                    # no hay match posible por ahora en este símbolo
                    break

                # hay match: se retiran ambas órdenes de sus heaps
                heapq.heappop(buy_heap)
                heapq.heappop(sell_heap)

                # el precio acordado es el de la orden más antigua (menor _seq),
                # es decir, quien llega después "toma" el precio de quien ya
                # estaba esperando en el libro
                if buy_seq < sell_seq:
                    agreed_price = buy_order.price
                else:
                    agreed_price = sell_order.price

                transaction = Transaction(
                    buy_order, sell_order, buy_order.quantity, agreed_price
                )
                self._transactions.append(transaction)
                yield transaction

    def transactions(self):
        for transaction in self._transactions:
            yield transaction
